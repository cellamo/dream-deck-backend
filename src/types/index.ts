export interface User {
    id: string;
    username: string;
    email: string;
    password: string;
  }
  
  export interface Dream {
    id: string;
    title: string;
    content: string;
    date: Date;
    emotions: string[];
    themes: string[];
    userId: string;
  }