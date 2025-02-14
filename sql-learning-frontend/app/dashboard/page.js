"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import AuthModal from "@/components/AuthModal";

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
        router.push("/"); // ✅ Redirect to home page if no user data
        return;
      }

      setUserId(storedUserId);
      setUserEmail(storedUserEmail);

      if (storedUserId) {
        async function fetchCurriculum() {
          try {
            const response = await axios.get(`http://127.0.0.1:8000/curriculum/${storedUserId}`);
            const lessons = response.data.lessons.sort((a, b) => a.id - b.id);
            setCurriculum(lessons);

            // Calculate progress
            const completedLessons = lessons.filter(lesson => lesson.completed).length;
            const progressPercentage = lessons.length > 0 ? (completedLessons / lessons.length) * 100 : 0;
            setProgress(progressPercentage);

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
    router.push("/"); // ✅ Redirect to home after logout
  };

  const handleLessonClick = (lessonId) => {
    router.push(`/lessons?lesson_id=${lessonId}`);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      
      {/* Signup Button in Top Right Corner */}
      <div className="absolute top-6 right-6">
        {!userEmail && <AuthModal initialMode="signup" />}
        {userEmail && (<button
          onClick={handleLogout}
          className="px-4 py-2 bg-red-600 text-white font-semibold rounded-lg shadow-md hover:bg-red-700"
        >
          Log Out
        </button>
        )}
      </div>
      
      {/* Main Content */}
      <div className="p-6 max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-blue-500">Your SQL Learning Plan</h1>

        {userEmail && (
          <div className="mt-4">
            <p className="text-gray-700">Logged in as: <strong>{userEmail}</strong></p>
          </div>
        )}

        {/* Progress Bar */}
        <div className="relative w-full bg-gray-200 rounded-full h-4 mt-6">
          <div className="bg-blue-600 h-4 rounded-full" style={{ width: `${progress}%` }}></div>
        </div>
        <p className="text-gray-700 text-sm mt-2">{Math.round(progress)}% completed</p>

        {/* Lessons List */}
        <ul className="mt-6 space-y-2">
          {curriculum.map((lesson, index) => (
            <li
              key={index}
              onClick={() => handleLessonClick(lesson.id)}
              className={`p-3 bg-gray-100 rounded-lg shadow cursor-pointer hover:bg-gray-200 ${lesson.completed ? 'line-through text-gray-500' : ''}`}
            >
              {index+1}. {lesson.title}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
