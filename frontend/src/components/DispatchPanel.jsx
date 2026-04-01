import React from 'react';
import { Truck, MapPin } from 'lucide-react';

export default function DispatchPanel({ routeData }) {
  if (!routeData) return <div className="panel">Loading route...</div>;

  return (
    <div className="panel">
      <div className="panel-header">
        <Truck size={24} color="#3b82f6" />
        Optimized Dispatch Route
      </div>
      
      <div style={{ marginBottom: '20px', color: '#94a3b8', fontSize: '0.9rem' }}>
        <div>Vehicle: <strong>{routeData.truck_id}</strong></div>
        <div>Total Distance: <strong>{routeData.logistics.total_route_distance} units</strong></div>
        <div>Deliveries: <strong>{routeData.deliveries_scheduled} stops</strong></div>
      </div>

      <div className="route-list">
        {routeData.logistics.route_steps.map((step, index) => {
          const isHub = index === 0 || index === routeData.logistics.route_steps.length - 1;
          
          return (
            <div key={index} className={`route-step ${isHub ? 'hub' : ''}`}>
              <div className="step-header">
                <div className="step-name">
                  {index + 1}. {step.farm_name}
                </div>
                <div className="step-distance">
                  {step.distance_from_previous > 0 ? `+${step.distance_from_previous} units` : 'Start'}
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#94a3b8', fontSize: '0.8rem' }}>
                <MapPin size={14} /> {step.farm_id}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
