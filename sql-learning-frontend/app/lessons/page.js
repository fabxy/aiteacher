"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkBreaks from "remark-breaks";


export default function LessonPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const lessonId = searchParams.get("lesson_id"); 
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sqlQuery, setSqlQuery] = useState("");
  const [queryResult, setQueryResult] = useState(null);
  const [error, setError] = useState(null);

  // Fetch lesson details when the component mounts or when lessonId changes
  useEffect(() => {
    if (!lessonId) {
      router.push("/dashboard");
      return;
    }

    async function fetchLesson() {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/lessons/${lessonId}`);
        setLesson(response.data);
      } catch (err) {
        console.error("Error fetching lesson details:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchLesson();
  }, [lessonId, router]);

  // Navigate back to the dashboard
  const handleBack = () => {
    router.push("/dashboard");
  };

  // Submit the SQL query to the backend
  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    setQueryResult(null);
    setError(null);

    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/lessons/${lessonId}/run_query`,
        { query: sqlQuery }
      );
      setQueryResult(response.data);
    } catch (err) {
      console.error("Error running SQL query:", err);
      setError("Error running SQL query. Please check your query and try again.");
    }
  };

  // Mark the lesson as complete in the backend
  const handleMarkComplete = async () => {
    try {
      await axios.put(`http://127.0.0.1:8000/lessons/${lessonId}/complete`);
      // Update local state to reflect completion
      setLesson((prevLesson) => ({ ...prevLesson, completed: true }));
      router.push("/dashboard");
    } catch (err) {
      console.error("Error marking lesson complete:", err);
    }
  };

  if (loading) return <p className="p-6">Generating personalized lesson...</p>;
  if (!lesson) return <p className="p-6">Lesson not found.</p>;

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Navigation */}
      <div className="absolute top-6 left-6">
        <button
          onClick={handleBack}
          className="px-4 py-2 bg-gray-600 text-white rounded-lg shadow-md hover:bg-gray-700"
        >
          Back to Dashboard
        </button>
      </div>

      {/* Lesson Content */}
      <div className="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow">
        {/* <h1 className="text-3xl font-bold mb-4">{lesson.title}</h1> */}
        <ReactMarkdown className="prose prose-lg max-w-none" remarkPlugins={[remarkGfm, remarkBreaks]}>
          {lesson.content || "This lesson has no content yet."}
        </ReactMarkdown>

        {/* SQL Exercise Section (if applicable) */}
        <div className="mb-6">
          <h2 className="text-2xl font-semibold mb-2">SQL Exercise</h2>
          <p className="mb-2">
            Try writing a SQL query to complete the exercise below:
          </p>
          <form onSubmit={handleQuerySubmit}>
            <textarea
              value={sqlQuery}
              onChange={(e) => setSqlQuery(e.target.value)}
              placeholder="Write your SQL query here..."
              className="w-full h-32 p-2 border rounded-md mb-2"
            ></textarea>
            <button
              type="submit"
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
            >
              Run Query
            </button>
          </form>
          {error && <p className="text-red-600 mt-2">{error}</p>}
          {queryResult && (
            <div className="mt-4">
              <h3 className="font-semibold">Query Result:</h3>
              <pre className="bg-gray-100 p-2 rounded">
                {JSON.stringify(queryResult, null, 2)}
              </pre>
            </div>
          )}
        </div>

        {/* Lesson Completion */}
        {!lesson.completed ? (
          <button
            onClick={handleMarkComplete}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700"
          >
            Mark as Complete
          </button>
        ) : (
          <p className="text-green-600 font-semibold">Lesson Completed</p>
        )}
      </div>
    </div>
  );
}
