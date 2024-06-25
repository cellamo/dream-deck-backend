// src/services/authService.ts

import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';
import { PrismaClient } from '@prisma/client';
import { User } from '../types';

const prisma = new PrismaClient();

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';

export const authService = {
  async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, 10);
  },

  async comparePasswords(plainTextPassword: string, hashedPassword: string): Promise<boolean> {
    return bcrypt.compare(plainTextPassword, hashedPassword);
  },

  generateToken(user: User): string {
    return jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '1d' });
  },

  verifyToken(token: string): { userId: string } {
    return jwt.verify(token, JWT_SECRET) as { userId: string };
  },

  async getUserFromToken(token: string): Promise<User | null> {
    try {
      const decoded = this.verifyToken(token);
      return prisma.user.findUnique({ where: { id: decoded.userId } }) as Promise<User | null>;
    } catch (error) {
      return null;
    }
  },
};