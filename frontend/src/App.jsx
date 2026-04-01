import React, { useState, useEffect } from 'react';
import './App.css';
import DispatchPanel from './components/DispatchPanel';
import InventoryPanel from './components/InventoryPanel';

function App() {
  const [inventoryStatus, setInventoryStatus] = useState([]);
  const [routePlan, setRoutePlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLogisticsData = async () => {
      try {
        // Fetch the raw inventory data
        const invResponse = await fetch('http://localhost:8000/api/inventory/status');
        if (!invResponse.ok) throw new Error('Inventory API failed');
        const invData = await invResponse.json();
        
        // Fetch the optimized routing data
        const routeResponse = await fetch('http://localhost:8000/api/logistics/daily-route');
        if (!routeResponse.ok) throw new Error('Routing API failed');
        const routeData = await routeResponse.json();

        setInventoryStatus(invData.data);
        setRoutePlan(routeData);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setError("Failed to connect to the logistics engine. Ensure the Python backend is running on port 8000.");
        setLoading(false);
      }
    };

    fetchLogisticsData();
  }, []);

  if (loading) return <div style={{ padding: '40px', color: 'white' }}>Initializing AgLogix Engine...</div>;
  if (error) return <div style={{ padding: '40px', color: '#ef4444' }}>{error}</div>;

  return (
    <div className="dashboard-layout">
      <DispatchPanel routeData={routePlan} />
      <InventoryPanel inventoryData={inventoryStatus} />
    </div>
  );
}

export default App;
