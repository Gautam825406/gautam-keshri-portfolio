export interface Profile {
  id: number;
  name: string;
  title: string;
  summary: string;
  email: string;
  linkedin: string;
  github: string;
  location: string;
  education: string;
  certification: string;
}

export interface Project {
  id: number;
  title: string;
  description: string;
  measured: string;
  live_url: string;
  github_url: string;
  stack: string[];
  sort_order: number;
}

export interface SkillGroup {
  category: string;
  items: string[];
}
