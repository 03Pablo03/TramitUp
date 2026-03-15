import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { LoginForm } from '@/components/auth/LoginForm'
import { AuthProvider } from '@/context/AuthContext'

// Mock fetch
global.fetch = jest.fn()

const MockedLoginForm = () => (
  <AuthProvider>
    <LoginForm />
  </AuthProvider>
)

describe('LoginForm', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    ;(global.fetch as jest.Mock).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ access_token: 'token', refresh_token: 'refresh' })
    })
  })

  it('renders login form with all fields', () => {
    render(<MockedLoginForm />)

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/contraseña/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /iniciar sesión/i })).toBeInTheDocument()
    expect(screen.getByText(/¿olvidaste tu contraseña/i)).toBeInTheDocument()
    expect(screen.getByText(/continuar con google/i)).toBeInTheDocument()
  })

  it('validates required fields', async () => {
    const user = userEvent.setup()
    render(<MockedLoginForm />)

    const submitButton = screen.getByRole('button', { name: /iniciar sesión/i })
    
    await user.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/el email es obligatorio/i)).toBeInTheDocument()
      expect(screen.getByText(/la contraseña es obligatoria/i)).toBeInTheDocument()
    })
  })

  it('validates email format', async () => {
    const user = userEvent.setup()
    render(<MockedLoginForm />)

    const emailInput = screen.getByLabelText(/email/i)
    const submitButton = screen.getByRole('button', { name: /iniciar sesión/i })

    await user.type(emailInput, 'invalid-email')
    await user.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/email no válido/i)).toBeInTheDocument()
    })
  })

  it('submits form with valid data', async () => {
    const user = userEvent.setup()
    render(<MockedLoginForm />)

    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/contraseña/i)
    const submitButton = screen.getByRole('button', { name: /iniciar sesión/i })

    await user.type(emailInput, 'test@example.com')
    await user.type(passwordInput, 'password123')
    await user.click(submitButton)

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/api/auth/signin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ email: 'test@example.com', password: 'password123' })
      })
    })
  })

  it('shows loading state during submission', async () => {
    const user = userEvent.setup()
    
    // Mock slow response
    ;(global.fetch as jest.Mock).mockImplementation(() => 
      new Promise(resolve => setTimeout(() => resolve({
        ok: true,
        json: () => Promise.resolve({ access_token: 'token', refresh_token: 'refresh' })
      }), 100))
    )

    render(<MockedLoginForm />)

    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/contraseña/i)
    const submitButton = screen.getByRole('button', { name: /iniciar sesión/i })

    await user.type(emailInput, 'test@example.com')
    await user.type(passwordInput, 'password123')
    await user.click(submitButton)

    // Should show loading state
    expect(screen.getByText(/iniciando sesión/i)).toBeInTheDocument()
    expect(submitButton).toBeDisabled()
  })

  it('displays error message on login failure', async () => {
    const user = userEvent.setup()
    
    ;(global.fetch as jest.Mock).mockResolvedValue({
      ok: false,
      json: () => Promise.resolve({ detail: 'Credenciales inválidas' })
    })

    render(<MockedLoginForm />)

    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/contraseña/i)
    const submitButton = screen.getByRole('button', { name: /iniciar sesión/i })

    await user.type(emailInput, 'test@example.com')
    await user.type(passwordInput, 'wrongpassword')
    await user.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/credenciales inválidas/i)).toBeInTheDocument()
    })
  })

  it('handles Google sign in', async () => {
    const user = userEvent.setup()
    render(<MockedLoginForm />)

    const googleButton = screen.getByText(/continuar con google/i)
    await user.click(googleButton)

    // Should trigger Google OAuth flow (mocked in jest.setup.js)
    // The actual implementation would redirect to Google
  })

  it('handles forgot password link', async () => {
    const user = userEvent.setup()
    render(<MockedLoginForm />)

    const forgotLink = screen.getByText(/¿olvidaste tu contraseña/i)
    expect(forgotLink).toHaveAttribute('href', '/login/forgot')
  })
})