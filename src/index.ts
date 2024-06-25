import express from 'express';
import { ApolloServer } from 'apollo-server-express';
import { PrismaClient } from '@prisma/client';
import fs from 'fs';
import path from 'path';
import { resolvers } from './resolvers';
import { authService } from './services/authService';

const prisma = new PrismaClient();

const typeDefs = fs.readFileSync(
  path.join(__dirname, 'schema', 'schema.graphql'),
  'utf8'
);

async function startServer() {
  const app = express() as any;

  const server = new ApolloServer({
    typeDefs,
    resolvers,
    context: async ({ req }) => {
      const token = req.headers.authorization?.split(' ')[1] || '';
      const user = await authService.getUserFromToken(token);
      return { prisma, user };
    },
  });

  await server.start();

  server.applyMiddleware({ app, path: '/graphql' });

  const PORT = process.env.PORT || 4000;

  app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}${server.graphqlPath}`);
  });
}

startServer().catch((error) => {
  console.error('Error starting server:', error);
});