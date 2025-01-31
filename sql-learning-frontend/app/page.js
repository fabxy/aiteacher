"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import axios from "axios";
import Image from "next/image";

export default function Home() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    sqlExperience: "",
    programmingExperience: "",
    learningCommitment: "",
  });

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedUserId = localStorage.getItem("userId");
      if (storedUserId) {
        router.push("/dashboard");  // ✅ Redirect returning users to dashboard
      }
    }
  }, [router]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleGenerate = async () => {
    setLoading(true);

    const formattedData = {
      sql_experience: formData.sqlExperience || "No experience provided",
      programming_experience: formData.programmingExperience || "No experience provided",
      learning_commitment: formData.learningCommitment || "No commitment specified",
    };

    console.log("Sending data:", formData); // ✅ Log the request body

    try {
      const response = await axios.post("http://127.0.0.1:8000/users/generate_curriculum/", formattedData);
      console.log("Response received:", response.data);
      const userId = response.data.user_id;
      localStorage.setItem("userId", userId);
      router.push("/dashboard");
    } catch (error) {
      console.error("Error generating curriculum:", error.response?.data || error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 text-center bg-gray-50">

    {/* Login Button (For returning users) */}
    <button
        onClick={() => router.push("/login")}
        className="absolute top-4 right-4 px-4 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700"
      >
        Log In
      </button>
      
      <h1 className="text-5xl font-bold text-blue-600">Learn SQL with Squirrel Steven</h1>
      <p className="mt-4 text-lg text-gray-700">A personalized, AI-powered learning experience tailored just for you.</p>

      <Image src="/squirrel_sql_teacher_brown.jpg" alt="Squirrel Steven" width={300} height={300} className="mt-6 rounded-lg shadow-lg" />

      <motion.div className="mt-10 bg-white p-6 rounded-lg shadow-md max-w-lg w-full">
        <h2 className="text-2xl font-semibold text-gray-900">Tell us about yourself</h2>

        <input type="text" name="sqlExperience" placeholder="Describe your SQL experience" onChange={handleChange} className="w-full p-3 border rounded-lg mt-3" />
        <input type="text" name="programmingExperience" placeholder="Describe your programming experience" onChange={handleChange} className="w-full p-3 border rounded-lg mt-3" />
        <input type="text" name="learningCommitment" placeholder="Time commitment per week (e.g., 5 hours)" onChange={handleChange} className="w-full p-3 border rounded-lg mt-3" />

        <motion.button 
          onClick={handleGenerate} 
          whileHover={{ scale: 1.05 }} 
          whileTap={{ scale: 0.95 }}
          className="w-full py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 mt-4"
        >
          {loading ? "Generating..." : "Generate Personalized Curriculum"}
        </motion.button>
      </motion.div>
    </div>
  );
}
