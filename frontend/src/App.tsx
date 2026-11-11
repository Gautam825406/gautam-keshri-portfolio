import { useEffect, useState } from "react";
import { api, adminKey, setAdminKey } from "./api";
import type { Profile, Project, SkillGroup } from "./types";

function usePortfolio() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [skills, setSkills] = useState<SkillGroup[]>([]);
  const [error, setError] = useState("");

  const load = async () => {
    try {
      const [p, pr, s] = await Promise.all([
        api.getProfile(),
        api.getProjects(),
        api.getSkills(),
      ]);
      setProfile(p);
      setProjects(pr);
      setSkills(s);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load portfolio");
    }
  };

  useEffect(() => {
    load();
  }, []);

  return { profile, projects, skills, error, reload: load };
}

function PublicPage() {
  const { profile, projects, skills, error } = usePortfolio();

  if (error) return <div className="container"><p className="error">{error} — is the backend running on :8000?</p></div>;
  if (!profile) return <div className="container"><p>Loading…</p></div>;

  return (
    <div>
      <header className="topbar">
        <span className="brand">{profile.name}</span>
        <nav>
          <a href="#projects">Projects</a>
          <a href="#skills">Skills</a>
          <a href="#contact">Contact</a>
          <a href="/admin">Admin</a>
        </nav>
      </header>

      <main className="container">
        <div className="hero">
          <h1>
            Hi, I&apos;m {profile.name.split(" ")[0]}. <span>I build production AI systems that are measured, not just demoed.</span>
          </h1>
          <p className="subtitle">{profile.title}</p>
          <p>{profile.summary}</p>
          <p className="meta">{profile.education} · {profile.location}</p>
          <div className="cta">
            <a className="btn" href="#projects">View projects</a>
            <a className="btn ghost" href={profile.github} target="_blank" rel="noreferrer">GitHub</a>
            <a className="btn ghost" href={profile.linkedin} target="_blank" rel="noreferrer">LinkedIn</a>
          </div>
        </div>

        <section id="projects">
          <h2>Projects</h2>
          <p className="lead">Flagship first — every project links to its live demo and source code.</p>
          <div className="grid">
            {projects.map((p, i) => (
              <article key={p.id} className={`card${i < 5 ? " flagship" : ""}`}>
                <h3>{p.title}</h3>
                <p>{p.description}</p>
                {p.measured ? <div className="measured">{p.measured}</div> : null}
                <div className="tags">
                  {p.stack.map((t) => (
                    <span key={t} className="tag">{t}</span>
                  ))}
                </div>
                <div className="links">
                  {p.live_url ? <a href={p.live_url} target="_blank" rel="noreferrer">Live Demo ↗</a> : null}
                  {p.github_url ? <a href={p.github_url} target="_blank" rel="noreferrer">GitHub ↗</a> : null}
                </div>
              </article>
            ))}
          </div>
        </section>

        <section id="skills">
          <h2>Skills</h2>
          <p className="lead">The stack behind the projects above.</p>
          <div className="skills-grid">
            {skills.map((g) => (
              <div key={g.category} className="skill-group">
                <h3>{g.category}</h3>
                <div className="tags">
                  {g.items.map((item) => (
                    <span key={item} className="tag">{item}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        <section>
          <h2>Education</h2>
          <p>{profile.education}</p>
          <p>{profile.certification}</p>
        </section>

        <footer id="contact">
          <strong>Contact</strong>
          <p>
            <a href={`mailto:${profile.email}`}>{profile.email}</a>
            <a href={profile.linkedin} target="_blank" rel="noreferrer">LinkedIn ↗</a>
            <a href={profile.github} target="_blank" rel="noreferrer">GitHub ↗</a>
          </p>
          <p>{profile.name} · {profile.location} · Seeking AI Engineer / Generative AI Intern roles.</p>
        </footer>
      </main>
    </div>
  );
}

const EMPTY_PROJECT: Omit<Project, "id"> = {
  title: "", description: "", measured: "", live_url: "", github_url: "", stack: [], sort_order: 0,
};

function AdminPage() {
  const { profile, projects, skills, reload } = usePortfolio();
  const [key, setKey] = useState(adminKey());
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [editing, setEditing] = useState<(Omit<Project, "id"> & { id?: number }) | null>(null);
  const [profileForm, setProfileForm] = useState<Omit<Profile, "id"> | null>(null);
  const [skillText, setSkillText] = useState("");

  useEffect(() => {
    if (profile && !profileForm) {
      const { id: _id, ...rest } = profile;
      setProfileForm(rest);
    }
  }, [profile, profileForm]);

  useEffect(() => {
    if (skills.length) {
      setSkillText(skills.map((g) => `${g.category}: ${g.items.join(", ")}`).join("\n"));
    }
  }, [skills]);

  const saveKey = () => {
    setAdminKey(key);
    setMessage("Admin key saved in this browser tab only (sessionStorage). It is never stored on the server.");
  };

  const parseSkills = (): SkillGroup[] =>
    skillText
      .split("\n")
      .map((line) => {
        const [category, rest] = line.split(":");
        return { category: (category || "").trim(), items: (rest || "").split(",").map((s) => s.trim()).filter(Boolean) };
      })
      .filter((g) => g.category);

  const run = async (fn: () => Promise<unknown>, ok: string) => {
    setError("");
    setMessage("");
    try {
      await fn();
      setMessage(ok);
      await reload();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Save failed — check the admin key (401 means wrong key).");
    }
  };

  if (!profile) return <div className="container"><p>Loading…</p></div>;

  return (
    <div className="container admin-box">
      <h1>Portfolio Admin</h1>
      <p><a href="/">← Back to public site</a> · Changes here update the live site immediately — no rebuild needed.</p>

      <label>Admin key</label>
      <input type="password" value={key} onChange={(e) => setKey(e.target.value)} placeholder="X-Admin-Key (from backend .env ADMIN_KEY)" />
      <button className="btn" onClick={saveKey}>Save key in this browser</button>
      <p className="notice">The key is kept only in this tab&apos;s sessionStorage. Wrong key → the API returns 401 on save.</p>
      {message ? <p className="notice">{message}</p> : null}
      {error ? <p className="error">{error}</p> : null}

      <h2>Projects</h2>
      {projects.map((p) => (
        <div key={p.id} className="admin-card">
          <h3>{p.title}</h3>
          <p>{p.description}</p>
          <button className="btn small" onClick={() => setEditing({ ...p })}>Edit</button>{" "}
          <button className="btn small danger" onClick={() => run(() => api.deleteProject(p.id), `Deleted ${p.title}.`)}>Delete</button>
        </div>
      ))}
      <button className="btn ghost" onClick={() => setEditing({ ...EMPTY_PROJECT, sort_order: projects.length })}>+ Add project</button>

      {editing ? (
        <div className="admin-card">
          <h3>{editing.id ? `Edit: ${editing.title}` : "New project"}</h3>
          <label>Title</label>
          <input value={editing.title} onChange={(e) => setEditing({ ...editing, title: e.target.value })} />
          <label>Description</label>
          <textarea value={editing.description} onChange={(e) => setEditing({ ...editing, description: e.target.value })} />
          <label>Measured eval line (leave blank if none — never invent numbers)</label>
          <textarea value={editing.measured} onChange={(e) => setEditing({ ...editing, measured: e.target.value })} />
          <label>Live URL</label>
          <input value={editing.live_url} onChange={(e) => setEditing({ ...editing, live_url: e.target.value })} />
          <label>GitHub URL</label>
          <input value={editing.github_url} onChange={(e) => setEditing({ ...editing, github_url: e.target.value })} />
          <label>Stack (comma-separated)</label>
          <input value={editing.stack.join(", ")} onChange={(e) => setEditing({ ...editing, stack: e.target.value.split(",").map((s) => s.trim()).filter(Boolean) })} />
          <label>Sort order</label>
          <input type="number" value={editing.sort_order} onChange={(e) => setEditing({ ...editing, sort_order: Number(e.target.value) })} />
          <button className="btn" onClick={() => run(
            async () => {
              if (editing.id) await api.updateProject(editing.id, editing);
              else await api.createProject(editing);
              setEditing(null);
            },
            "Project saved.",
          )}>Save project</button>{" "}
          <button className="btn ghost" onClick={() => setEditing(null)}>Cancel</button>
        </div>
      ) : null}

      <h2>Profile</h2>
      {profileForm ? (
        <div className="admin-card">
          {(["name", "title", "location", "email", "linkedin", "github"] as const).map((f) => (
            <div key={f}>
              <label>{f}</label>
              <input value={profileForm[f]} onChange={(e) => setProfileForm({ ...profileForm, [f]: e.target.value })} />
            </div>
          ))}
          <label>Summary</label>
          <textarea value={profileForm.summary} onChange={(e) => setProfileForm({ ...profileForm, summary: e.target.value })} />
          <label>Education</label>
          <input value={profileForm.education} onChange={(e) => setProfileForm({ ...profileForm, education: e.target.value })} />
          <label>Certification</label>
          <input value={profileForm.certification} onChange={(e) => setProfileForm({ ...profileForm, certification: e.target.value })} />
          <button className="btn" onClick={() => run(() => api.updateProfile(profileForm), "Profile saved.")}>Save profile</button>
        </div>
      ) : null}

      <h2>Skills</h2>
      <div className="admin-card">
        <label>One group per line — “Category: item, item, item”</label>
        <textarea value={skillText} onChange={(e) => setSkillText(e.target.value)} style={{ minHeight: 140 }} />
        <button className="btn" onClick={() => run(() => api.updateSkills(parseSkills()), "Skills saved.")}>Save skills</button>
      </div>
    </div>
  );
}

export default function App() {
  const isAdmin = window.location.pathname.startsWith("/admin");
  return isAdmin ? <AdminPage /> : <PublicPage />;
}
