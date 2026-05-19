import { createContext, useContext, useState, useEffect } from 'react'
import { api } from '../lib/api'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    if (typeof window === 'undefined') return null
    const saved = localStorage.getItem('skillradar-user')
    return saved ? JSON.parse(saved) : null
  })

  useEffect(() => {
    if (user) {
      localStorage.setItem('skillradar-user', JSON.stringify(user))
    } else {
      localStorage.removeItem('skillradar-user')
    }
  }, [user])

  const login = async (email, fullName = '', college = '') => {
    const { data } = await api.post('/api/users/register', {
      email, full_name: fullName, college,
    })
    setUser(data.user)
    return data.user
  }

  const logout = () => setUser(null)

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
