// src/resolvers/index.ts

import { PrismaClient } from '@prisma/client';
import { User, Dream } from '../types';
import { authService } from '../services/authService';

const prisma = new PrismaClient();

export const resolvers = {
  Query: {
    /* getUser: async (_: any, { id }: { id: string }, context: { user: User | null }) => {
      if (!context.user) throw new Error('Not authenticated');
      return prisma.user.findUnique({
        where: { id },
        include: { dreams: true },
      });
    }, */
    getUser: async (_: any, { id }: { id: string }, context: { prisma: PrismaClient }) => {
      return context.prisma.user.findUnique({
        where: { id },
        include: { dreams: true },
      });
    },
    
    getDream: async (_: any, { id }: { id: string }, context: { user: User | null }) => {
      if (!context.user) throw new Error('Not authenticated');
      return prisma.dream.findUnique({
        where: { id },
        include: { user: true },
      });
    },
    getUserDreams: async (_: any, { userId }: { userId: string }, context: { user: User | null }) => {
      if (!context.user) throw new Error('Not authenticated');
      if (context.user.id !== userId) throw new Error('Not authorized');
      return prisma.dream.findMany({
        where: { userId },
        orderBy: { date: 'desc' },
      });
    },
  },
  Mutation: {
    signup: async (_: any, { username, email, password }: { username: string; email: string; password: string }) => {
      const hashedPassword = await authService.hashPassword(password);
      const user = await prisma.user.create({
        data: { username, email, password: hashedPassword },
      });
      const token = authService.generateToken(user as User);
      return { user, token };
    },
    login: async (_: any, { email, password }: { email: string; password: string }) => {
      const user = await prisma.user.findUnique({ where: { email } });
      if (!user) throw new Error('Invalid credentials');
      const isValidPassword = await authService.comparePasswords(password, user.password);
      if (!isValidPassword) throw new Error('Invalid credentials');
      const token = authService.generateToken(user as User);
      return { user, token };
    },
    createDream: async (_: any, { title, content, date, emotions, themes }: { title: string; content: string; date: string; emotions: string[]; themes: string[] }, context: { user: User | null }) => {
      if (!context.user) throw new Error('Not authenticated');
      return prisma.dream.create({
        data: {
          title,
          content,
          date: new Date(date),
          emotions,
          themes,
          user: { connect: { id: context.user.id } },
        },
      });
    },
    updateDream: async (_: any, { id, title, content, emotions, themes }: { id: string; title?: string; content?: string; emotions?: string[]; themes?: string[] }, context: { user: User | null }) => {
      if (!context.user) throw new Error('Not authenticated');
      const dream = await prisma.dream.findUnique({ where: { id } });
      if (!dream || dream.userId !== context.user.id) throw new Error('Not authorized');
      return prisma.dream.update({
        where: { id },
        data: { title, content, emotions, themes },
      });
    },
    deleteDream: async (_: any, { id }: { id: string }, context: { user: User | null }) => {
      if (!context.user) throw new Error('Not authenticated');
      const dream = await prisma.dream.findUnique({ where: { id } });
      if (!dream || dream.userId !== context.user.id) throw new Error('Not authorized');
      await prisma.dream.delete({ where: { id } });
      return true;
    },
  },
};