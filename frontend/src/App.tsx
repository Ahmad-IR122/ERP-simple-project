import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignOutButton,
  UserButton,
  useAuth,
} from "@clerk/clerk-react"
import { api } from "./api/api"

function App() {
  const { getToken, isSignedIn } = useAuth()

  const testBackend = async () => {
    try {
      if (!isSignedIn) {
        console.log("User is not signed in")
        return
      }

      const token = await getToken()

      if (!token) {
        console.error("Unable to obtain Clerk token")
        return
      }

      const response = await api.get("/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      console.log("Backend response:", response.data)
    } catch (error) {
      console.error("Backend request failed:", error)
    }
  }

  return (
    <div>
      <SignedOut>
        <SignInButton mode="modal">
          <button>Sign In</button>
        </SignInButton>
      </SignedOut>

      <SignedIn>
        <UserButton />

        <SignOutButton>
          <button>Sign Out</button>
        </SignOutButton>

        <button onClick={testBackend}>
          Test protected API
        </button>
      </SignedIn>
    </div>
  )
}

export default App
