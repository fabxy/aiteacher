"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

export default function Dashboard() {
  const router = useRouter();
  const [curriculum, setCurriculum] = useState([]);
  const [progress, setProgress] = useState(0);
  const [userId, setUserId] = useState(null);
  const [userEmail, setUserEmail] = useState(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedUserId = localStorage.getItem("userId");
      const storedUserEmail = localStorage.getItem("userEmail");

      if (!storedUserId && !storedUserEmail) {
        router.push("/");  // ✅ Redirect to home page if no user data
        return;
      }

      setUserId(storedUserId);
      setUserEmail(storedUserEmail);

      if (storedUserId) {
        async function fetchCurriculum() {
          try {
            const response = await axios.get(`http://127.0.0.1:8000/users/curriculum/${storedUserId}`);
            const lessons = JSON.parse(response.data.lessons);
            setCurriculum(lessons);
          } catch (error) {
            console.error("Error fetching curriculum:", error);
          }
        }
        fetchCurriculum();
      }
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("userId");
    localStorage.removeItem("userEmail");
    router.push("/");  // ✅ Redirect to home after logout
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold">Your SQL Learning Plan</h1>

      {/* If the user is signed up, show email and logout button */}
      {userEmail ? (
        <div className="mt-4">
          <p className="text-gray-700">Logged in as: <strong>{userEmail}</strong></p>
          <button
            onClick={handleLogout}
            className="mt-4 px-6 py-3 bg-red-600 text-white rounded-lg text-lg shadow-md hover:bg-red-700"
          >
            Log Out
          </button>
        </div>
      ) : (
        // If user is not signed up, show a "Sign Up to Save Progress" button
        userId && (
          <button
            onClick={() => router.push(`/signup?user_id=${userId}`)}
            className="mt-4 px-6 py-3 bg-green-600 text-white rounded-lg text-lg shadow-md hover:bg-green-700 w-full"
          >
            Sign Up to Save Progress
          </button>
        )
      )}

      {/* Progress Bar */}
      <div className="relative w-full bg-gray-200 rounded-full h-4 mt-6">
        <div className="bg-blue-600 h-4 rounded-full" style={{ width: `${progress}%` }}></div>
      </div>
      <p className="text-gray-700 text-sm mt-2">{progress}% completed</p>

      {/* Lessons List */}
      <ul className="mt-6 space-y-2">
        {curriculum.map((lesson, index) => (
          <li key={index} className="p-3 bg-gray-100 rounded-lg shadow">{lesson}</li>
        ))}
      </ul>
    </div>
  );
}
