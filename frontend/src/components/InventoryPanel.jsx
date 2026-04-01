import React from 'react';
import { Activity } from 'lucide-react';

export default function InventoryPanel({ inventoryData }) {
  if (!inventoryData || inventoryData.length === 0) return <div className="panel">Loading telemetry...</div>;

  return (
    <div className="panel">
      <div className="panel-header">
        <Activity size={24} color="#10b981" />
        Silo Telemetry & Forecasting
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Location</th>
              <th>Current Volume</th>
              <th>Capacity</th>
              <th>Run-Out Forecast</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {inventoryData.map((farm) => (
              <tr key={farm.farm_id}>
                <td>
                  <div style={{ fontWeight: 500 }}>{farm.farm_name}</div>
                  <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{farm.farm_id}</div>
                </td>
                <td style={{ width: '25%' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                    <span>{farm.current_tons} tons</span>
                    <span>{farm.fill_percentage}%</span>
                  </div>
                  <div className="progress-bar-bg">
                    <div 
                      className={`progress-bar-fill ${farm.needs_delivery ? 'critical' : ''}`}
                      style={{ width: `${farm.fill_percentage}%` }}
                    ></div>
                  </div>
                </td>
                <td>{farm.capacity_tons} tons</td>
                <td>
                  <strong style={{ color: farm.needs_delivery ? '#ef4444' : '#e2e8f0' }}>
                    {farm.days_remaining} days
                  </strong>
                </td>
                <td>
                  {farm.needs_delivery ? (
                    <span className="status-badge status-critical">DISPATCH REQUIRED</span>
                  ) : (
                    <span className="status-badge status-ok">OPTIMAL</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
