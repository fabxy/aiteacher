import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import * as Dialog from "@radix-ui/react-dialog";

export default function AuthModal({ initialMode = "login" }) {
  const isLogin = useState(initialMode === "login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const resetFields = () => {
    setEmail("");
    setPassword("");
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("handleSubmit");
    setError(""); // Clear previous errors

    try {
      if (isLogin) {
        // Login request
        const response = await axios.post("http://127.0.0.1:8000/users/login/", {
          email,
          password,
        });

        localStorage.setItem("userEmail", email);
        localStorage.setItem("userId", response.data.user_id);
        router.push("/dashboard"); // Redirect to dashboard

      } else {
        // Signup request
        const userId = localStorage.getItem("userId");

        await axios.post("http://127.0.0.1:8000/users/signup/", {
          user_id: parseInt(userId, 10),
          email,
          password,
        });

        localStorage.setItem("userEmail", email); // Save email in local storage
        window.location.reload();
      }
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred"); // Handle API errors
    }
  };

  return (
    <Dialog.Root onOpenChange={(isOpen) => !isOpen && resetFields()}>
      <Dialog.Trigger className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 mt-4">
        {isLogin ? "Log In" : "Sign Up"}
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black bg-opacity-50" />
        <Dialog.Content className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 p-6 bg-white rounded-lg shadow-lg w-96">
          <Dialog.Title className="text-xl font-semibold mb-4">
            {isLogin ? "Log In" : "Sign Up"}
          </Dialog.Title>

          <form className="flex flex-col gap-3" onSubmit={handleSubmit}>
            <input
              type="email"
              placeholder="Email"
              className="border p-2 rounded"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              className="border p-2 rounded"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            {error && <p className="text-red-500 mb-2">{error}</p>}
            
            <button type="submit" className="bg-blue-500 text-white py-2 rounded">
              {isLogin ? "Log In" : "Sign Up"}
            </button>
          </form>

          <Dialog.Close className="absolute top-2 right-2 text-gray-500">✖</Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
