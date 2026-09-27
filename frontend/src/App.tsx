import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignOutButton,
  UserButton,
  useAuth,
} from "@clerk/clerk-react";
import { api } from "./api/api";

function App() {
  const { getToken, isSignedIn } = useAuth();

  const testAdmin = async () => {
    try {
      if (!isSignedIn) {
        console.log("User is not signed in");
        return;
      }

      const token = await getToken();

      const response = await api.get("/admin-test", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      console.log("Admin response:", response.data);
    } catch (error) {
      console.error("Admin test failed:", error);
    }
  };
  const testBackend = async () => {
    try {
      if (!isSignedIn) {
        console.log("User is not signed in");
        return;
      }

      const token = await getToken();

      console.log("CLERK TOKEN:", token);

      const response = await api.get("/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      console.log("Backend response:", response.data);
    } catch (error) {
      console.error("Backend request failed:", error);
    }
  };

  const testEmployee = async () =>{
    try {
        if (!isSignedIn) {
        console.log("User is not signed in");
        return;
      }

      const token = await getToken();

      const response = await api.get("/employee-test", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      console.log("Employee response:", response.data);
    } catch (error) {
      console.error("Employee test failed:", error);

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

        <button onClick={testBackend}>Test protected API</button>
        <button onClick={testEmployee}>Test Employee Access</button>
      </SignedIn>

      <button onClick={testAdmin}>Test Admin Access</button>
    </div>
  );
}

export default App;
