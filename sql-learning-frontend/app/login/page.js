"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

export default function Login() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleLogin = async () => {
    setErrorMessage(""); // Reset error message

    try {
      const response = await axios.post("http://127.0.0.1:8000/users/login/", {
        email,
        password,
      });

      // ✅ Store user info in localStorage
      localStorage.setItem("userEmail", email);
      localStorage.setItem("userId", response.data.user_id);

      router.push("/dashboard"); // ✅ Redirect to dashboard
    } catch (error) {
      setErrorMessage("Invalid email or password");
      console.error("Login failed:", error.response?.data || error);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 text-center bg-gray-50">
      <h1 className="text-3xl font-bold text-blue-600">Login</h1>
      <p className="text-gray-700 mt-2">Welcome back! Please log in to continue.</p>

      <input
        type="email"
        placeholder="Enter your email"
        onChange={(e) => setEmail(e.target.value)}
        className="w-full p-3 border rounded-lg mt-6"
      />

      <input
        type="password"
        placeholder="Enter your password"
        onChange={(e) => setPassword(e.target.value)}
        className="w-full p-3 border rounded-lg mt-4"
      />

      {errorMessage && <p className="text-red-500 mt-2">{errorMessage}</p>}

      <button
        onClick={handleLogin}
        className="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg text-lg shadow-md hover:bg-blue-700"
      >
        Login
      </button>

      <p className="mt-4 text-gray-600">
        Don't have an account?{" "}
        <a href="/" className="text-blue-600 hover:underline">
            Get started here
        </a>
      </p>
    </div>
  );
}
