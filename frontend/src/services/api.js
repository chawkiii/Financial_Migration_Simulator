// frontend/src/services/api.js

import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const runSimulation = async (data) => {
  const response = await api.post("/simulate", data);
  return response.data;
};

export default api;