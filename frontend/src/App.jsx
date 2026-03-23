// frontend/src/App.jsx

import { SimulationProvider } from "./context/SimulationContext.jsx";
import Dashboard from "./components/Dashboard.jsx";

function App() {
  return (
    <SimulationProvider>
      <Dashboard />
    </SimulationProvider>
  );
}

export default App;