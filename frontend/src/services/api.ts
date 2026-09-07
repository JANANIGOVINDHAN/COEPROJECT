import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const getDashboardSummary = () => api.get('/dashboard/summary').then(r => r.data);
export const getDriftFindings = (params?: any) => api.get('/drift/findings', { params }).then(r => r.data);
export const triggerDriftScan = () => api.post('/drift/scan').then(r => r.data);
export const getSites = () => api.get('/sites').then(r => r.data);
export const getDevices = () => api.get('/devices').then(r => r.data);
export const getBaselines = () => api.get('/baselines').then(r => r.data);
export const getComplianceRules = () => api.get('/compliance/rules').then(r => r.data);
export const getChangeTickets = () => api.get('/tickets').then(r => r.data);
export const getAuditLogs = () => api.get('/audit/logs').then(r => r.data);
