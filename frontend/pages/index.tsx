import { useState, useEffect } from 'react';
import Head from 'next/head';
import { authAPI, taskAPI } from '../utils/api';
import { SimpleChatWidget } from '../src/components/SimpleChatWidget';
import { TestChat } from '../src/components/TestChat';

// Define TypeScript interfaces
interface User {
  user_id: string;
  email: string;
  created_at: string;
}

interface Task {
  task_id: string;
  user_id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

export default function Home() {
  const [user, setUser] = useState<User | null>(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  const [token, setToken] = useState<string | null>(null);

  // Edit task state
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');

  // Check for existing token on component mount
  useEffect(() => {
    // Only run on client-side to avoid SSR issues
    if (typeof window !== 'undefined') {
      const storedToken = localStorage.getItem('token');
      if (storedToken) {
        setToken(storedToken);
        fetchTasks();
      }
    }
  }, []);

  // Fetch tasks for authenticated user
  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await taskAPI.getTasks();
      setTasks(response.data);
    } catch (err: any) {
      setError('Failed to fetch tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle registration
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await authAPI.register(email, password);
      setUser(response.data);
      setError('');
    } catch (err: any) {
      console.error('Registration error:', err);
      let errorMessage = 'Registration failed';
      if (err.response?.data?.detail) {
        errorMessage = `Registration failed: ${err.response.data.detail}`;
      } else if (err.message) {
        errorMessage = `Registration failed: ${err.message}`;
      }
      setError(errorMessage);
    }
  };

  // Handle login
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await authAPI.login(email, password);

      // Backend returns AuthToken with access_token field
      const authToken = response.data.access_token;
      setToken(authToken);
      localStorage.setItem('token', authToken);
      fetchTasks();
      setError('');
    } catch (err: any) {
      console.error('Login error:', err);
      let errorMessage = 'Login failed';
      if (err.response?.data?.detail) {
        errorMessage = `Login failed: ${err.response.data.detail}`;
      } else if (err.message) {
        errorMessage = `Login failed: ${err.message}`;
      }
      setError(errorMessage);
    }
  };

  // Handle logout
  const handleLogout = () => {
    authAPI.logout();
    setToken(null);
    setUser(null);
    setTasks([]);
    setEmail('');
    setPassword('');
  };

  // Create a new task
  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) return;

    try {
      const response = await taskAPI.createTask(title, description);
      setTasks([...tasks, response.data]);
      setTitle('');
      setDescription('');
      setError('');
    } catch (err: any) {
      console.error('Create task error:', err);
      let errorMessage = 'Failed to create task';
      if (err.response?.data?.detail) {
        errorMessage = `Failed to create task: ${err.response.data.detail}`;
      } else if (err.message) {
        errorMessage = `Failed to create task: ${err.message}`;
      }
      setError(errorMessage);
    }
  };

  // Start editing a task
  const startEditing = (task: Task) => {
    setEditingTaskId(task.task_id);
    setEditTitle(task.title);
    setEditDescription(task.description || '');
  };

  // Cancel editing
  const cancelEditing = () => {
    setEditingTaskId(null);
    setEditTitle('');
    setEditDescription('');
    setError('');
  };

  // Update a task
  const handleUpdateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token || !editingTaskId) return;

    try {
      const response = await taskAPI.updateTask(editingTaskId, editTitle, editDescription);

      setTasks(tasks.map(task =>
        task.task_id === editingTaskId ? response.data : task
      ));

      cancelEditing();
      setError('');
    } catch (err: any) {
      console.error('Update task error:', err);
      let errorMessage = 'Failed to update task';
      if (err.response?.data?.detail) {
        errorMessage = `Failed to update task: ${err.response.data.detail}`;
      } else if (err.message) {
        errorMessage = `Failed to update task: ${err.message}`;
      }
      setError(errorMessage);
    }
  };

  // Toggle task completion
  const toggleTaskCompletion = async (taskId: string) => {
    if (!token) return;

    try {
      const response = await taskAPI.toggleTask(taskId);

      setTasks(tasks.map(task =>
        task.task_id === taskId ? response.data : task
      ));
      setError('');
    } catch (err: any) {
      console.error('Toggle task error:', err);
      let errorMessage = 'Failed to update task';
      if (err.response?.data?.detail) {
        errorMessage = `Failed to update task: ${err.response.data.detail}`;
      } else if (err.message) {
        errorMessage = `Failed to update task: ${err.message}`;
      }
      setError(errorMessage);
    }
  };

  // Delete a task
  const handleDeleteTask = async (taskId: string) => {
    if (!token) return;

    try {
      await taskAPI.deleteTask(taskId);
      setTasks(tasks.filter(task => task.task_id !== taskId));
      setError('');
    } catch (err: any) {
      console.error('Delete task error:', err);
      let errorMessage = 'Failed to delete task';
      if (err.response?.data?.detail) {
        errorMessage = `Failed to delete task: ${err.response.data.detail}`;
      } else if (err.message) {
        errorMessage = `Failed to delete task: ${err.message}`;
      }
      setError(errorMessage);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>Todo App</title>
        <meta name="description" content="A full-stack todo application" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Todo App</h1>
          {token && (
            <button
              onClick={handleLogout}
              className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
            >
              Logout
            </button>
          )}
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {!token ? (
          // Authentication Section
          <div className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md">
            <div className="flex mb-6">
              <button
                className={`flex-1 py-2 px-4 rounded-l ${
                  authMode === 'login' ? 'bg-blue-500 text-white' : 'bg-gray-200'
                }`}
                onClick={() => setAuthMode('login')}
              >
                Login
              </button>
              <button
                className={`flex-1 py-2 px-4 rounded-r ${
                  authMode === 'register' ? 'bg-blue-500 text-white' : 'bg-gray-200'
                }`}
                onClick={() => setAuthMode('register')}
              >
                Register
              </button>
            </div>

            <form onSubmit={authMode === 'login' ? handleLogin : handleRegister}>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  required
                />
              </div>
              <div className="mb-6">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
                  required
                  minLength={8}
                />
              </div>
              <div className="flex items-center justify-between">
                <button
                  type="submit"
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
                >
                  {authMode === 'login' ? 'Login' : 'Register'}
                </button>
              </div>
            </form>
          </div>
        ) : (
          // Todo List Section
          <div className="max-w-2xl mx-auto">
            <div className="bg-white shadow rounded-lg p-6 mb-6">
              <h2 className="text-xl font-bold mb-4">Create New Task</h2>
              <form onSubmit={handleCreateTask}>
                <div className="mb-4">
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="Task title"
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-2"
                    required
                  />
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Task description (optional)"
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    rows={2}
                  />
                </div>
                <button
                  type="submit"
                  className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
                >
                  Add Task
                </button>
              </form>
            </div>

            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-bold mb-4">Your Tasks</h2>
              {loading ? (
                <p>Loading tasks...</p>
              ) : tasks.length === 0 ? (
                <p>No tasks yet. Create your first task!</p>
              ) : (
                <ul className="divide-y divide-gray-200">
                  {tasks.map((task) => (
                    <li key={task.task_id} className="py-4">
                      {editingTaskId === task.task_id ? (
                        <form onSubmit={handleUpdateTask} className="w-full">
                          <div className="flex flex-col mb-2">
                             <input
                              type="text"
                              value={editTitle}
                              onChange={(e) => setEditTitle(e.target.value)}
                              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-2"
                              required
                            />
                            <textarea
                              value={editDescription}
                              onChange={(e) => setEditDescription(e.target.value)}
                              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-2"
                              rows={2}
                            />
                          </div>
                          <div className="flex justify-end space-x-2">
                            <button
                              type="button"
                              onClick={cancelEditing}
                              className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-1 px-3 rounded text-sm"
                            >
                              Cancel
                            </button>
                            <button
                              type="submit"
                              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-3 rounded text-sm"
                            >
                              Save
                            </button>
                          </div>
                        </form>
                      ) : (
                        <div>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center">
                              <input
                                type="checkbox"
                                checked={task.is_completed}
                                onChange={() => toggleTaskCompletion(task.task_id)}
                                className="h-4 w-4 text-blue-600 rounded"
                              />
                              <span
                                className={`ml-3 text-lg ${
                                  task.is_completed ? 'line-through text-gray-500' : 'text-gray-900'
                                }`}
                              >
                                {task.title}
                              </span>
                            </div>
                            <div className="flex space-x-2">
                              <button
                                onClick={() => startEditing(task)}
                                className="text-blue-500 hover:text-blue-700"
                              >
                                Edit
                              </button>
                              <button
                                onClick={() => handleDeleteTask(task.task_id)}
                                className="text-red-500 hover:text-red-700"
                              >
                                Delete
                              </button>
                            </div>
                          </div>
                          {task.description && (
                            <p className="ml-7 text-gray-600 text-sm mt-1">{task.description}</p>
                          )}
                        </div>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        )}
      </main>

      {/* AI Chatbot Widget */}
      {token && <SimpleChatWidget onTaskUpdate={fetchTasks} />}
    </div>
  );
}