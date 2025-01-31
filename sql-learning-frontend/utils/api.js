import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; // Adjust if deployed

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Fetch lessons
export const getLessons = async () => {
  const response = await api.get("/lessons/");
  return response.data;
};

// Register user
export const registerUser = async (email, password) => {
  return await api.post("/users/register/", { email, password });
};

// Execute SQL query
export const executeSQL = async (query) => {
  return await api.post("/sql/run/", { query });
};
