"use client";
import { useState } from "react";
import { executeSQL } from "../../utils/api";
import CodeMirror from "@uiw/react-codemirror";
import { sql } from "@codemirror/lang-sql";

export default function SQLEditorPage() {
  const [query, setQuery] = useState("SELECT * FROM users;");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const runQuery = async () => {
    try {
      const response = await executeSQL(query);
      setResult(response.data.result);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.error || "An error occurred");
      setResult(null);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-blue-600 mb-6">SQL Playground</h1>

      <CodeMirror
        value={query}
        height="200px"
        extensions={[sql()]}
        onChange={(value) => setQuery(value)}
        className="border rounded-lg"
      />

      <button onClick={runQuery} className="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700">
        Run Query
      </button>

      {result && (
        <div className="mt-6 p-4 bg-gray-100 rounded-lg shadow">
          <h2 className="text-lg font-semibold">Results:</h2>
          <pre className="text-sm">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}

      {error && <p className="text-red-500 mt-4">{error}</p>}
    </div>
  );
}
