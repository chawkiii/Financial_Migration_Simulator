// frontend/src/services/api.js

import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const runSimulation = async (data) => {
  try {
    const response = await api.post("/simulate", data);
    return response.data;
  } catch (err) {
    console.error("Simulation API error:", err);
    throw err;
  }
};

export default api;