export interface ScalixAuthConfig {
  url: string
  autoRefresh?: boolean
  persistSession?: boolean
  storageKey?: string
  /**
   * CL5: in-memory / httpOnly-cookie mode. When true (browser only), the refresh
   * token is NEVER stored in localStorage — the access token lives only in memory
   * and the refresh token rides the gateway's httpOnly `scalix_refresh` cookie
   * (XSS-safe). Refresh uses the double-submit CSRF token (`scalix_csrf` cookie →
   * `x-scalix-csrf` header); the session is silently restored from the cookie on
   * construct. Requires the gateway `/v1/auth` cookie plane (default in prod).
   */
  useCookies?: boolean
}

export interface AuthResponse {
  user: User
  session: Session
}

export interface User {
  id: string
  email?: string
  phone?: string
  is_anonymous: boolean
  raw_user_meta_data: Record<string, unknown>
  created_at: string
  updated_at: string
}

export interface Session {
  access_token: string
  refresh_token: string
  expires_in: number
  expires_at: string
  token_type: string
}

type AuthChangeEvent = 'SIGNED_IN' | 'SIGNED_OUT' | 'TOKEN_REFRESHED' | 'USER_UPDATED'
type AuthChangeCallback = (event: AuthChangeEvent, session: Session | null) => void

export class ScalixAuthClient {
  private url: string
  private session: Session | null = null
  private user: User | null = null
  private listeners: Set<AuthChangeCallback> = new Set()
  private refreshTimer: ReturnType<typeof setTimeout> | null = null
  private storageKey: string
  private autoRefresh: boolean
  private persistSession: boolean
  private useCookies: boolean

  constructor(config: ScalixAuthConfig) {
    this.url = config.url.replace(/\/$/, '')
    this.storageKey = config.storageKey ?? 'scalix-auth-session'
    this.autoRefresh = config.autoRefresh ?? true
    this.useCookies = config.useCookies ?? false
    // In cookie mode nothing is persisted client-side (the httpOnly cookie IS the
    // durable credential), so persistSession is forced off.
    this.persistSession = this.useCookies ? false : (config.persistSession ?? true)

    if (typeof window !== 'undefined') {
      if (this.useCookies) {
        // Silently restore the session from the httpOnly refresh cookie.
        void this.refreshSession()
      } else if (this.persistSession) {
        this.loadSession()
      }
    }
  }

  private getCsrfToken(): string {
    if (typeof document === 'undefined') return ''
    const m = document.cookie.match(/(?:^|;\s*)scalix_csrf=([^;]+)/)
    return m ? decodeURIComponent(m[1]) : ''
  }

  async signUp(email: string, password: string, data?: Record<string, unknown>): Promise<AuthResponse> {
    const resp = await this.post('/v1/auth/signup', { email, password, data })
    this.setSession(resp)
    return resp
  }

  async signInWithPassword(email: string, password: string): Promise<AuthResponse> {
    const resp = await this.post('/v1/auth/login', { email, password })
    this.setSession(resp)
    return resp
  }

  async signInWithOtp(phone: string): Promise<void> {
    await this.post('/v1/auth/otp', { phone })
  }

  async verifyOtp(phone: string, token: string): Promise<AuthResponse> {
    const resp = await this.post('/v1/auth/otp/verify', { phone, token })
    this.setSession(resp)
    return resp
  }

  async signInWithMagicLink(email: string): Promise<void> {
    await this.post('/v1/auth/magic-link', { email })
  }

  async signInWithOAuth(provider: string, redirectUrl: string): Promise<{ url: string }> {
    return this.fetchJson('/v1/auth/oauth/authorize', { provider, redirect_url: redirectUrl })
  }

  async signInAnonymously(): Promise<AuthResponse> {
    const resp = await this.post('/v1/auth/anonymous', {})
    this.setSession(resp)
    return resp
  }

  async signOut(): Promise<void> {
    // In cookie mode we may have no in-memory session but still hold a server
    // session behind the httpOnly cookie — always attempt the server-side logout.
    if (this.session || this.useCookies) {
      try {
        const headers: Record<string, string> = {}
        if (this.useCookies) {
          const csrf = this.getCsrfToken()
          if (csrf) headers['x-scalix-csrf'] = csrf
        }
        await this.fetch('/v1/auth/logout', { method: 'POST', headers, body: JSON.stringify({}) })
      } catch {
        // ignore signout errors
      }
    }
    this.clearSession()
  }

  async getUser(): Promise<User | null> {
    if (!this.session) return null
    try {
      const resp = await this.fetch('/v1/auth/user', { method: 'GET' })
      this.user = resp as User
      return this.user
    } catch {
      return null
    }
  }

  async updateUser(attrs: { email?: string; password?: string; data?: Record<string, unknown> }): Promise<User> {
    const resp = await this.fetch('/v1/auth/user', {
      method: 'PUT',
      body: JSON.stringify(attrs),
    })
    const result = resp as User
    this.user = result
    this.notify('USER_UPDATED')
    return result
  }

  async refreshSession(): Promise<Session | null> {
    const bodyToken = this.session?.refresh_token
    // Body-token path needs a stored refresh token; cookie mode refreshes from the
    // httpOnly cookie with no stored token.
    if (!bodyToken && !this.useCookies) return null
    try {
      const headers: Record<string, string> = {}
      const body: Record<string, unknown> = {}
      if (bodyToken) {
        // Bearer-style: the gateway reads the token from the body (no CSRF needed).
        body.refresh_token = bodyToken
      } else {
        // Cookie/ambient credential: double-submit CSRF (echo the readable cookie).
        const csrf = this.getCsrfToken()
        if (csrf) headers['x-scalix-csrf'] = csrf
      }
      // /v1/auth/refresh returns a bare Session (not { user, session }); it rotates
      // the httpOnly refresh + CSRF cookies on the response.
      const session = await this.fetch('/v1/auth/refresh', {
        method: 'POST',
        headers,
        body: JSON.stringify(body),
      }) as Session
      if (!session?.access_token) {
        this.clearSession()
        return null
      }
      this.session = session
      this.saveSession()
      this.scheduleRefresh()
      this.notify('TOKEN_REFRESHED')
      return this.session
    } catch {
      this.clearSession()
      return null
    }
  }

  getSession(): Session | null {
    return this.session
  }

  getCurrentUser(): User | null {
    return this.user
  }

  onAuthStateChange(callback: AuthChangeCallback): { unsubscribe: () => void } {
    this.listeners.add(callback)
    return { unsubscribe: () => this.listeners.delete(callback) }
  }

  // ── MFA ──

  async enrollMfa(factorType: string = 'totp', friendlyName?: string): Promise<{ id: string; totp: { qr_code: string; uri: string } }> {
    return this.fetchJson('/v1/auth/mfa/enroll', { factor_type: factorType, friendly_name: friendlyName })
  }

  async verifyMfa(factorId: string, code: string): Promise<void> {
    await this.post('/v1/auth/mfa/verify', { factor_id: factorId, code })
  }

  async challengeMfa(factorId: string, code: string): Promise<AuthResponse> {
    const resp = await this.post('/v1/auth/mfa/challenge', { factor_id: factorId, code })
    this.setSession(resp)
    return resp
  }

  // ── Internals ──

  private async post(path: string, body: Record<string, unknown>): Promise<AuthResponse> {
    const resp = await this.fetch(path, {
      method: 'POST',
      body: JSON.stringify(body),
    })
    return resp as AuthResponse
  }

  private async fetchJson<T>(path: string, body: Record<string, unknown>): Promise<T> {
    const resp = await this.fetch(path, {
      method: 'POST',
      body: JSON.stringify(body),
    })
    return resp as T
  }

  private async fetch(path: string, init: RequestInit): Promise<unknown> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }
    if (this.session?.access_token) {
      headers['Authorization'] = `Bearer ${this.session.access_token}`
    }
    const resp = await globalThis.fetch(`${this.url}${path}`, {
      // CL5: send/receive the gateway's httpOnly refresh + CSRF cookies in browser
      // consumers (harmless in Node where there are no cookies). This lets a browser
      // app rely on the httpOnly cookie instead of a JS-readable refresh token.
      credentials: 'include',
      ...init,
      headers: { ...headers, ...(init.headers as Record<string, string> ?? {}) },
    })
    if (!resp.ok) {
      const body = await resp.json().catch(() => ({}))
      const msg = (body as Record<string, unknown>)?.error ?? `Request failed: ${resp.status}`
      throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg))
    }
    return resp.json()
  }

  private setSession(resp: AuthResponse, event: AuthChangeEvent = 'SIGNED_IN') {
    this.session = resp.session
    this.user = resp.user
    this.saveSession()
    this.scheduleRefresh()
    this.notify(event)
  }

  private clearSession() {
    this.session = null
    this.user = null
    if (this.refreshTimer) clearTimeout(this.refreshTimer)
    this.refreshTimer = null
    if (this.persistSession && typeof window !== 'undefined') {
      localStorage.removeItem(this.storageKey)
    }
    this.notify('SIGNED_OUT')
  }

  private saveSession() {
    if (!this.persistSession || typeof window === 'undefined' || !this.session) return
    localStorage.setItem(this.storageKey, JSON.stringify({
      session: this.session,
      user: this.user,
    }))
  }

  private loadSession() {
    try {
      const raw = localStorage.getItem(this.storageKey)
      if (!raw) return
      const data = JSON.parse(raw)
      if (data?.session?.access_token) {
        const expiresAt = new Date(data.session.expires_at).getTime()
        if (expiresAt > Date.now()) {
          this.session = data.session
          this.user = data.user
          this.scheduleRefresh()
        } else if (data.session.refresh_token) {
          this.session = data.session
          this.user = data.user
          this.refreshSession()
        }
      }
    } catch {
      // corrupted storage
    }
  }

  private scheduleRefresh() {
    if (!this.autoRefresh || !this.session) return
    if (this.refreshTimer) clearTimeout(this.refreshTimer)

    const expiresAt = new Date(this.session.expires_at).getTime()
    const refreshIn = Math.max((expiresAt - Date.now()) - 60_000, 5_000)

    this.refreshTimer = setTimeout(() => this.refreshSession(), refreshIn)
  }

  private notify(event: AuthChangeEvent) {
    for (const cb of this.listeners) {
      try { cb(event, this.session) } catch { /* listener error */ }
    }
  }
}
