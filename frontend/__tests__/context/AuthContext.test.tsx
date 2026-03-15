import React from 'react'
import { render, screen, waitFor, act } from '@testing-library/react'
import { AuthProvider, useAuth } from '@/context/AuthContext'

// Mock fetch globally
global.fetch = jest.fn()

// Test component that uses AuthContext
function TestComponent() {
  const { user, loading, signInWithEmail, signOut } = useAuth()
  
  return (
    <div>
      <div data-testid="loading">{loading ? 'loading' : 'not-loading'}</div>
      <div data-testid="user">{user ? user.email : 'no-user'}</div>
      <button onClick={() => signInWithEmail('test@example.com', 'password')}>
        Sign In
      </button>
      <button onClick={signOut}>Sign Out</button>
    </div>
  )
}

describe('AuthContext', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    // Mock successful fetch response
    ;(global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ access_token: 'token', refresh_token: 'refresh' })
    })
  })

  it('provides auth context to children', async () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    // Initially should be loading
    expect(screen.getByTestId('loading')).toHaveTextContent('loading')
    expect(screen.getByTestId('user')).toHaveTextContent('no-user')

    // Wait for loading to finish
    await waitFor(() => {
      expect(screen.getByTestId('loading')).toHaveTextContent('not-loading')
    })
  })

  it('handles sign in with email', async () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    await waitFor(() => {
      expect(screen.getByTestId('loading')).toHaveTextContent('not-loading')
    })

    const signInButton = screen.getByText('Sign In')
    
    await act(async () => {
      signInButton.click()
    })

    // Should call fetch with correct parameters
    expect(global.fetch).toHaveBeenCalledWith('/api/auth/signin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email: 'test@example.com', password: 'password' })
    })
  })

  it('handles sign out', async () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    await waitFor(() => {
      expect(screen.getByTestId('loading')).toHaveTextContent('not-loading')
    })

    const signOutButton = screen.getByText('Sign Out')
    
    await act(async () => {
      signOutButton.click()
    })

    // Should reset user state
    expect(screen.getByTestId('user')).toHaveTextContent('no-user')
  })

  it('throws error when used outside provider', () => {
    // Suppress console.error for this test
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation()

    expect(() => {
      render(<TestComponent />)
    }).toThrow('useAuth must be used within AuthProvider')

    consoleSpy.mockRestore()
  })

  it('handles server fallback when session loading fails', async () => {
    // Mock fetch for /api/auth/me endpoint
    ;(global.fetch as jest.Mock).mockImplementation((url) => {
      if (url === '/api/auth/me') {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            user: { id: '123', email: 'test@example.com' },
            access_token: 'server-token'
          })
        })
      }
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({})
      })
    })

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    // Wait for the 2-second timeout and server fallback
    await waitFor(() => {
      expect(screen.getByTestId('loading')).toHaveTextContent('not-loading')
    }, { timeout: 3000 })
  })
})