# SankofaLens build notes

## Architecture
Browser -> FastAPI API -> SQLAlchemy -> MySQL.

The frontend is intentionally framework-free: HTML, CSS and vanilla JavaScript. This keeps the hackathon implementation easy to explain and demonstrates full-stack fundamentals.

## Roles
- user: explore heritage, use passport, interact with Naa
- admin: create/update heritage sites and view operational dashboard
- superuser: all admin abilities plus user/role management

Role checks happen on the backend. Hiding a button in JavaScript is not considered security.

## Security
JWT is issued by the API and stored by the demo frontend in localStorage. For a production deployment, consider secure HttpOnly cookies, CSRF protection where applicable, rate limiting, refresh-token rotation, email verification and password reset flows.

## Naa
The API deliberately keeps the AI key server-side. The current endpoint is an integration boundary. The production version should retrieve approved heritage source material and pass only relevant context to the chosen model provider.

## QR
Each heritage site has a unique qr_code identifier. The next implementation step can generate physical QR images from `/api/sites/{id}/qr` and have the QR open a public experience route. The data model is already prepared for this flow.

## Content governance
Because heritage can be sensitive and contested, every production story should have provenance, an approval status, source references, contributor attribution and a review date. Community submissions should pass moderation before public publication.

## Recommended next additions
1. CMS interface for heritage editors.
2. QR image generation and scan analytics.
3. Offline/PWA support for low-connectivity sites.
4. Verified source citations per story.
5. Twi, Ga, Ewe and Dagbani translation workflow.
6. Audio narration and accessibility controls.
7. 360-degree tours and AR layer.
8. Booking/experience partner integration.
9. Automated tests and CI/CD.
10. Observability, backups and production secrets management.
