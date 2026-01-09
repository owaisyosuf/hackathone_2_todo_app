# Todo Frontend

A Next.js frontend for the Todo application with authentication and task management.

## Getting Started

First, install the dependencies:

```bash
npm install
```

Then, copy the environment file and configure your API URL:

```bash
cp .env.example .env.local
```

Finally, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Features

- User registration and authentication
- Task management (create, read, update, delete, toggle completion)
- Responsive design with Tailwind CSS
- TypeScript type safety

## Environment Variables

- `NEXT_PUBLIC_API_URL`: The URL of the backend API (default: http://localhost:8000)

## Learn More

To learn more about the technologies used in this project:

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)