# @scalix-world/auth

Client-side authentication for apps built on **Scalix Auth** — the end-user
auth surface of [Scalix Cloud](https://scalix.world) (signup/login, MFA, social
login, magic links, session management, token refresh).

This is the browser/client library your end-users' frontend uses. To manage
users from the server (admin: create/list/revoke), use the `auth` service on the
main [`@scalix-world/sdk`](https://www.npmjs.com/package/@scalix-world/sdk).

## Install

```bash
npm install @scalix-world/auth
```

## Usage

```typescript
import { ScalixAuthClient } from '@scalix-world/auth'

const auth = new ScalixAuthClient({ url: 'https://api.scalix.world' })

await auth.signUp('user@example.com', 'password')
const { user } = await auth.signInWithPassword('user@example.com', 'password')

// social login
const { url } = await auth.signInWithOAuth('google', 'https://myapp.com/callback')
window.location.href = url

// session
const session = auth.getSession()
auth.onAuthStateChange((event, session) => {
  console.log(event, session)
})
```

No API key — this is the end-user auth surface; users authenticate with their
own credentials against your Scalix Auth endpoint.

### httpOnly-cookie mode (browser)

By default the session persists in `localStorage`. For an XSS-safe setup, pass
`useCookies: true`: the access token lives only in memory, the refresh token
rides the gateway's httpOnly `scalix_refresh` cookie (with double-submit CSRF
protection), and the session is silently restored from the cookie on construct.

```typescript
const auth = new ScalixAuthClient({
  url: 'https://api.scalix.world',
  useCookies: true,
})
```

### React

```tsx
import { ScalixAuthProvider, useUser, useSession } from '@scalix-world/auth/react'

function App() {
  return (
    <ScalixAuthProvider client={auth}>
      <Profile />
    </ScalixAuthProvider>
  )
}

function Profile() {
  const user = useUser()
  return <span>{user?.email}</span>
}
```

## License

MIT
