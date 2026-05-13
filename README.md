# RideHailing Platform

Microservices architecture for a production ride-hailing application.

## Services
| Service | Language | Description |
|---------|----------|-------------|
| matching-service | Python | Driver-rider dispatch and ETA |
| tracking-service | Python | Real-time GPS with Kalman filtering |
| payments-service | Python | Stripe + UPI + wallet abstraction |
| pricing-service  | Python | Surge pricing engine |
| rider-app        | React Native | Rider-facing mobile app |
| driver-app       | React Native | Driver-facing mobile app |

## Tech Stack
- **API Gateway**: FastAPI + Uvicorn
- **Message Bus**: Apache Kafka
- **Cache**: Redis
- **Database**: PostgreSQL (per service)
- **Maps**: Google Maps SDK + OSRM for routing
- **Payments**: Stripe + Razorpay (UPI)
- **Push**: Firebase Cloud Messaging

## Getting Started
```bash
docker-compose up -d
```

## Team
| Name | Role | Owns |
|------|------|------|
| Mahindra Kshirsagar | Engineering Manager | Platform, architecture |
| Hema Yadav | Senior SWE | Matching engine, GPS tracking |
| Avani Kshirsagar | Senior SWE | Payments, pricing, safety |

## Team
| Name | Role | Domain |
|------|------|--------|
| Mahindra Kshirsagar | Engineering Manager | Platform & architecture |
| Hema Yadav | Senior SWE | Matching · GPS · Safety |
| Avani Kshirsagar | Senior SWE | Payments · Surge · Earnings |
