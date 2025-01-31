"use client";
import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import axios from "axios";

export default function Signup() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const userId = searchParams.get("user_id"); // ✅ Get user_id from URL
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = async () => {
    try {
      const payload = {
        user_id: parseInt(userId, 10),  // ✅ Ensure user_id is an integer
        email,
        password
      };
      
      console.log("Sending signup request:", payload);  // ✅ Debugging log
      
      await axios.post("http://127.0.0.1:8000/users/update_email/", payload);
  
      // ✅ Store email in localStorage to mark user as logged in
      localStorage.setItem("userEmail", email);
  
      router.push("/dashboard");
    } catch (error) {
      console.error("Signup failed:", error.response?.data || error);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 text-center bg-gray-50">
      <h1 className="text-3xl font-bold text-blue-600">Sign Up to Store Progress</h1>
      
      <input 
        type="email" 
        placeholder="Enter your email" 
        onChange={(e) => setEmail(e.target.value)} 
        className="w-full p-3 border rounded-lg mt-6"
      />

      <input 
        type="password" 
        placeholder="Create a password" 
        onChange={(e) => setPassword(e.target.value)} 
        className="w-full p-3 border rounded-lg mt-4"
      />

      <button 
        onClick={handleSignup} 
        className="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg text-lg shadow-md hover:bg-blue-700"
      >
        Create Account
      </button>
    </div>
  );
}
