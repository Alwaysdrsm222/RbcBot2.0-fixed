import React, { useState, useEffect } from 'react';
import './App.css';

const App = () => {
  const [giveaways, setGiveaways] = useState([]);
  const [isAdmin, setIsAdmin] = useState(false);
  const [adminPassword, setAdminPassword] = useState('');
  const [showAdminLogin, setShowAdminLogin] = useState(false);
  const [loading, setLoading] = useState(false);
  const [newGiveaway, setNewGiveaway] = useState({
    title: '',
    description: '',
    prize: '',
    endDate: '',
    entryRequirement: ''
  });

  const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    fetchGiveaways();
    const interval = setInterval(fetchGiveaways, 30000); // Auto-refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchGiveaways = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/giveaways`);
      if (response.ok) {
        const data = await response.json();
        setGiveaways(data);
      }
    } catch (error) {
      console.error('Error fetching giveaways:', error);
    }
  };

  const handleAdminLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/admin/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: adminPassword })
      });
      
      if (response.ok) {
        setIsAdmin(true);
        setShowAdminLogin(false);
        setAdminPassword('');
      } else {
        alert('Invalid admin password!');
      }
    } catch (error) {
      console.error('Admin login error:', error);
      alert('Login failed. Please try again.');
    }
    setLoading(false);
  };

  const handleAddGiveaway = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/admin/giveaways`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newGiveaway)
      });
      
      if (response.ok) {
        setNewGiveaway({
          title: '',
          description: '',
          prize: '',
          endDate: '',
          entryRequirement: ''
        });
        fetchGiveaways();
        alert('Giveaway added successfully!');
      }
    } catch (error) {
      console.error('Error adding giveaway:', error);
      alert('Failed to add giveaway. Please try again.');
    }
    setLoading(false);
  };

  const handleDeleteGiveaway = async (giveawayId) => {
    if (window.confirm('Are you sure you want to delete this giveaway?')) {
      try {
        const response = await fetch(`${backendUrl}/api/admin/giveaways/${giveawayId}`, {
          method: 'DELETE'
        });
        
        if (response.ok) {
          fetchGiveaways();
          alert('Giveaway deleted successfully!');
        }
      } catch (error) {
        console.error('Error deleting giveaway:', error);
        alert('Failed to delete giveaway. Please try again.');
      }
    }
  };

  const formatTimeRemaining = (endDate) => {
    const now = new Date();
    const end = new Date(endDate);
    const diff = end - now;
    
    if (diff <= 0) return 'ENDED';
    
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    
    return `${days}d ${hours}h ${minutes}m`;
  };

  const activeGiveaways = giveaways.filter(g => new Date(g.endDate) > new Date());

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-900 via-yellow-800 to-orange-900">
      {/* Animated Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-10 -left-10 w-72 h-72 bg-orange-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute -top-10 -right-10 w-72 h-72 bg-yellow-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-10 left-10 w-72 h-72 bg-orange-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      {/* Header */}
      <header className="relative z-10 p-6">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 rounded-full overflow-hidden border-4 border-orange-400 shadow-lg">
              <img 
                src="https://images.pexels.com/photos/792381/pexels-photo-792381.jpeg" 
                alt="RBC Logo" 
                className="w-full h-full object-cover"
              />
            </div>
            <h1 className="text-3xl font-bold text-white animate-pulse">RBC Community</h1>
          </div>
          <button
            onClick={() => setShowAdminLogin(true)}
            className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-2 rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl"
          >
            Admin Panel
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative z-10 text-center py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="mb-8">
            <img 
              src="https://images.unsplash.com/photo-1615963244664-5b845b2025ee?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODB8MHwxfHNlYXJjaHwxfHx0aWdlcnxlbnwwfHx8fDE3NTA2MTk2NDB8MA&ixlib=rb-4.1.0&q=85" 
              alt="RBC Tiger" 
              className="w-64 h-64 mx-auto rounded-full object-cover shadow-2xl border-8 border-orange-400 animate-bounce-slow"
            />
          </div>
          
          <h2 className="text-6xl font-bold text-white mb-6 animate-text-gradient bg-gradient-to-r from-orange-300 via-yellow-300 to-orange-300 bg-clip-text text-transparent">
            Welcome to RBC Community
          </h2>
          
          <p className="text-xl text-orange-100 mb-8 leading-relaxed">
            Join our fierce tiger community! 🐅 We're a chill gaming community with amazing giveaways, 
            friendly members, and endless fun. Ready to unleash your inner tiger?
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="https://discord.gg/letsgo"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-indigo-600 hover:bg-indigo-700 text-white text-xl font-bold px-8 py-4 rounded-full transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 animate-pulse"
            >
              🚀 Join Discord Server
            </a>
            <button
              onClick={() => document.getElementById('giveaways').scrollIntoView({ behavior: 'smooth' })}
              className="bg-orange-600 hover:bg-orange-700 text-white text-xl font-bold px-8 py-4 rounded-full transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              🎁 View Giveaways
            </button>
          </div>
        </div>
      </section>

      {/* Why Join Section */}
      <section className="relative z-10 py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-4xl font-bold text-center text-white mb-12">Why Join RBC Community?</h3>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-black bg-opacity-30 backdrop-blur-sm p-8 rounded-xl border border-orange-400 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105">
              <div className="text-5xl mb-4 text-center">🎁</div>
              <h4 className="text-2xl font-bold text-orange-300 mb-4 text-center">Epic Giveaways</h4>
              <p className="text-orange-100 text-center">Regular giveaways with amazing prizes. From gaming gear to exclusive items!</p>
            </div>
            <div className="bg-black bg-opacity-30 backdrop-blur-sm p-8 rounded-xl border border-orange-400 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105">
              <div className="text-5xl mb-4 text-center">👥</div>
              <h4 className="text-2xl font-bold text-orange-300 mb-4 text-center">Chill Community</h4>
              <p className="text-orange-100 text-center">Friendly, welcoming environment where everyone can have fun and make friends.</p>
            </div>
            <div className="bg-black bg-opacity-30 backdrop-blur-sm p-8 rounded-xl border border-orange-400 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105">
              <div className="text-5xl mb-4 text-center">🎮</div>
              <h4 className="text-2xl font-bold text-orange-300 mb-4 text-center">Gaming Fun</h4>
              <p className="text-orange-100 text-center">Join gaming sessions, tournaments, and connect with fellow gamers!</p>
            </div>
          </div>
        </div>
      </section>

      {/* Active Giveaways Section */}
      <section id="giveaways" className="relative z-10 py-16 px-6">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-4xl font-bold text-center text-white mb-12">🔥 Active Giveaways</h3>
          
          {activeGiveaways.length === 0 ? (
            <div className="text-center text-orange-200 text-xl">
              No active giveaways at the moment. Check back soon! 🐅
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {activeGiveaways.map((giveaway) => (
                <div key={giveaway.id} className="bg-black bg-opacity-40 backdrop-blur-sm p-6 rounded-xl border-2 border-orange-400 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105 animate-glow">
                  <div className="text-center mb-4">
                    <div className="text-3xl mb-2">🎁</div>
                    <h4 className="text-2xl font-bold text-orange-300 mb-2">{giveaway.title}</h4>
                    <p className="text-orange-100 mb-4">{giveaway.description}</p>
                    <div className="bg-gradient-to-r from-orange-500 to-yellow-500 text-white font-bold py-2 px-4 rounded-lg mb-4">
                      Prize: {giveaway.prize}
                    </div>
                    <div className="text-lg font-bold text-yellow-300 animate-pulse">
                      ⏰ {formatTimeRemaining(giveaway.endDate)}
                    </div>
                    <p className="text-orange-200 text-sm mt-2">
                      Entry: {giveaway.entryRequirement}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Community Stats */}
      <section className="relative z-10 py-16 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-4xl font-bold text-white mb-12">Community Stats</h3>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-black bg-opacity-30 backdrop-blur-sm p-6 rounded-xl border border-orange-400">
              <div className="text-4xl font-bold text-orange-300 mb-2">500+</div>
              <div className="text-orange-100">Active Members</div>
            </div>
            <div className="bg-black bg-opacity-30 backdrop-blur-sm p-6 rounded-xl border border-orange-400">
              <div className="text-4xl font-bold text-orange-300 mb-2">50+</div>
              <div className="text-orange-100">Giveaways Hosted</div>
            </div>
            <div className="bg-black bg-opacity-30 backdrop-blur-sm p-6 rounded-xl border border-orange-400">
              <div className="text-4xl font-bold text-orange-300 mb-2">24/7</div>
              <div className="text-orange-100">Community Support</div>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="relative z-10 py-20 px-6 text-center">
        <div className="max-w-4xl mx-auto">
          <h3 className="text-5xl font-bold text-white mb-8">Ready to Join the Pack? 🐅</h3>
          <a
            href="https://discord.gg/letsgo"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-gradient-to-r from-orange-500 to-yellow-500 hover:from-orange-600 hover:to-yellow-600 text-white text-2xl font-bold px-12 py-6 rounded-full transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-110 animate-bounce-slow inline-block"
          >
            🚀 Join RBC Discord Now!
          </a>
        </div>
      </section>

      {/* Admin Login Modal */}
      {showAdminLogin && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-xl shadow-2xl max-w-md w-full mx-4">
            <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">Admin Login</h3>
            <form onSubmit={handleAdminLogin}>
              <input
                type="password"
                placeholder="Enter admin password"
                value={adminPassword}
                onChange={(e) => setAdminPassword(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-orange-500"
                required
              />
              <div className="flex gap-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 bg-orange-600 hover:bg-orange-700 text-white py-3 rounded-lg transition-colors disabled:opacity-50"
                >
                  {loading ? 'Logging in...' : 'Login'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowAdminLogin(false);
                    setAdminPassword('');
                  }}
                  className="flex-1 bg-gray-400 hover:bg-gray-500 text-white py-3 rounded-lg transition-colors"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Admin Panel */}
      {isAdmin && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 overflow-y-auto">
          <div className="bg-white p-8 rounded-xl shadow-2xl max-w-4xl w-full mx-4 my-8">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-3xl font-bold text-gray-800">Admin Panel</h3>
              <button
                onClick={() => setIsAdmin(false)}
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors"
              >
                Close
              </button>
            </div>

            {/* Add New Giveaway Form */}
            <div className="mb-8 p-6 bg-gray-50 rounded-lg">
              <h4 className="text-xl font-bold text-gray-800 mb-4">Add New Giveaway</h4>
              <form onSubmit={handleAddGiveaway} className="grid md:grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="Giveaway Title"
                  value={newGiveaway.title}
                  onChange={(e) => setNewGiveaway({...newGiveaway, title: e.target.value})}
                  className="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                  required
                />
                <input
                  type="text"
                  placeholder="Prize Description"
                  value={newGiveaway.prize}
                  onChange={(e) => setNewGiveaway({...newGiveaway, prize: e.target.value})}
                  className="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                  required
                />
                <textarea
                  placeholder="Giveaway Description"
                  value={newGiveaway.description}
                  onChange={(e) => setNewGiveaway({...newGiveaway, description: e.target.value})}
                  className="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 md:col-span-2"
                  rows="3"
                  required
                />
                <input
                  type="datetime-local"
                  value={newGiveaway.endDate}
                  onChange={(e) => setNewGiveaway({...newGiveaway, endDate: e.target.value})}
                  className="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                  required
                />
                <input
                  type="text"
                  placeholder="Entry Requirement"
                  value={newGiveaway.entryRequirement}
                  onChange={(e) => setNewGiveaway({...newGiveaway, entryRequirement: e.target.value})}
                  className="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                  required
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="md:col-span-2 bg-orange-600 hover:bg-orange-700 text-white py-3 rounded-lg transition-colors disabled:opacity-50"
                >
                  {loading ? 'Adding...' : 'Add Giveaway'}
                </button>
              </form>
            </div>

            {/* Current Giveaways */}
            <div>
              <h4 className="text-xl font-bold text-gray-800 mb-4">Current Giveaways</h4>
              {giveaways.length === 0 ? (
                <p className="text-gray-600">No giveaways found.</p>
              ) : (
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {giveaways.map((giveaway) => (
                    <div key={giveaway.id} className="p-4 border border-gray-200 rounded-lg">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h5 className="font-bold text-lg">{giveaway.title}</h5>
                          <p className="text-gray-600 mb-2">{giveaway.description}</p>
                          <p className="text-orange-600 font-semibold">Prize: {giveaway.prize}</p>
                          <p className="text-sm text-gray-500">
                            Ends: {new Date(giveaway.endDate).toLocaleString()}
                          </p>
                          <p className="text-sm text-gray-500">Entry: {giveaway.entryRequirement}</p>
                        </div>
                        <button
                          onClick={() => handleDeleteGiveaway(giveaway.id)}
                          className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm transition-colors"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="relative z-10 bg-black bg-opacity-50 text-center py-8 px-6">
        <div className="max-w-4xl mx-auto">
          <p className="text-orange-200 mb-4">© 2025 RBC Community. All rights reserved.</p>
          <p className="text-orange-300">Built with 🧡 for our amazing tiger community!</p>
        </div>
      </footer>
    </div>
  );
};

export default App;