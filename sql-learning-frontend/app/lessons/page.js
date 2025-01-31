"use client";
import { useQuery } from "@tanstack/react-query";
import { getLessons } from "../../utils/api";

export default function Lessons() {
  const { data: lessons, isLoading, error } = useQuery({ queryKey: ["lessons"], queryFn: getLessons });

  if (isLoading) return <p className="text-center">Loading lessons...</p>;
  if (error) return <p className="text-center text-red-500">Failed to load lessons.</p>;

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-blue-600 mb-6">SQL Lessons</h1>
      <ul className="space-y-4">
        {lessons.map((lesson) => (
          <li key={lesson.id} className="p-4 bg-gray-100 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold">{lesson.title}</h2>
            <p className="text-gray-700">{lesson.content}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
