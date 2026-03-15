import '@testing-library/jest-dom'

// Mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: jest.fn(),
      replace: jest.fn(),
      prefetch: jest.fn(),
      back: jest.fn(),
      forward: jest.fn(),
      refresh: jest.fn(),
    }
  },
  useSearchParams() {
    return {
      get: jest.fn(),
    }
  },
  usePathname() {
    return ''
  },
}))

// Mock Supabase client
jest.mock('./lib/supabase/client', () => ({
  createClient: () => ({
    auth: {
      getSession: jest.fn().mockResolvedValue({ data: { session: null }, error: null }),
      getUser: jest.fn().mockResolvedValue({ data: { user: null }, error: null }),
      signInWithOAuth: jest.fn().mockResolvedValue({ data: {}, error: null }),
      signInWithOtp: jest.fn().mockResolvedValue({ data: {}, error: null }),
      signUp: jest.fn().mockResolvedValue({ data: {}, error: null }),
      signOut: jest.fn().mockResolvedValue({ error: null }),
      resetPasswordForEmail: jest.fn().mockResolvedValue({ data: {}, error: null }),
      setSession: jest.fn().mockResolvedValue({ data: {}, error: null }),
      onAuthStateChange: jest.fn().mockReturnValue({
        data: { subscription: { unsubscribe: jest.fn() } }
      }),
    },
    from: jest.fn().mockReturnValue({
      select: jest.fn().mockReturnValue({
        eq: jest.fn().mockReturnValue({
          single: jest.fn().mockResolvedValue({ data: null, error: null })
        })
      })
    })
  })
}))

// Mock API fetch
global.fetch = jest.fn()

// Mock window.location properties and methods
Object.defineProperty(window.location, 'assign', {
  value: jest.fn(),
  writable: true,
})

Object.defineProperty(window.location, 'replace', {
  value: jest.fn(),
  writable: true,
})

Object.defineProperty(window.location, 'reload', {
  value: jest.fn(),
  writable: true,
})