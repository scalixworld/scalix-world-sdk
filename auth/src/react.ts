import { createContext, useContext, useEffect, useState, useMemo, useCallback } from 'react'
import { createElement } from 'react'
import type { ReactNode } from 'react'
import type { ScalixAuthClient, User, Session, ScalixAuthConfig } from './client.js'

interface ScalixAuthContextValue {
  client: ScalixAuthClient
  user: User | null
  session: Session | null
  loading: boolean
  signUp: (email: string, password: string, data?: Record<string, unknown>) => Promise<void>
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
  signInAnonymously: () => Promise<void>
}

const ScalixAuthContext = createContext<ScalixAuthContextValue | null>(null)

interface ScalixAuthProviderProps {
  client: ScalixAuthClient
  children: ReactNode
}

export function ScalixAuthProvider({ client, children }: ScalixAuthProviderProps) {
  const [user, setUser] = useState<User | null>(client.getCurrentUser())
  const [session, setSession] = useState<Session | null>(client.getSession())
  const [loading, setLoading] = useState(!!client.getSession())

  useEffect(() => {
    const { unsubscribe } = client.onAuthStateChange((_event, sess) => {
      setSession(sess)
      setUser(client.getCurrentUser())
      setLoading(false)
    })

    if (client.getSession()) {
      client.getUser().then((u) => {
        setUser(u)
        setLoading(false)
      }).catch(() => setLoading(false))
    }

    return unsubscribe
  }, [client])

  const signUp = useCallback(async (email: string, password: string, data?: Record<string, unknown>) => {
    await client.signUp(email, password, data)
  }, [client])

  const signIn = useCallback(async (email: string, password: string) => {
    await client.signInWithPassword(email, password)
  }, [client])

  const signOut = useCallback(async () => {
    await client.signOut()
  }, [client])

  const signInAnonymously = useCallback(async () => {
    await client.signInAnonymously()
  }, [client])

  const value = useMemo<ScalixAuthContextValue>(() => ({
    client,
    user,
    session,
    loading,
    signUp,
    signIn,
    signOut,
    signInAnonymously,
  }), [client, user, session, loading, signUp, signIn, signOut, signInAnonymously])

  return createElement(ScalixAuthContext.Provider, { value }, children)
}

export function useScalixAuth(): ScalixAuthContextValue {
  const ctx = useContext(ScalixAuthContext)
  if (!ctx) throw new Error('useScalixAuth must be used within ScalixAuthProvider')
  return ctx
}

export function useUser(): User | null {
  return useScalixAuth().user
}

export function useSession(): Session | null {
  return useScalixAuth().session
}

export { ScalixAuthContext }
export type { ScalixAuthContextValue, ScalixAuthProviderProps, ScalixAuthConfig }
