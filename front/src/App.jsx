import React, { useEffect, useState } from 'react'

const App = () => {

  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const [currentUser, setCurrentUser] = useState(null)


  const handleSubmit = (e) => {
    e.preventDefault()

    if (username !== "" && password !== "") {
      login({ username, password })
    }
  }

  const login = (credentials) => {
    fetch('http://127.0.0.1:5000/api/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then((response) => response.json())
      .then((data) => {

        console.log(data)
        setCurrentUser(data.access_token)
        sessionStorage.setItem('access_token', data.access_token)


      })
      .catch((error) => console.log(error))
  }

  const logout = () => {
    setCurrentUser(null)
    sessionStorage.removeItem('access_token')
  }

  useEffect(() => {
    checkUser()
  }, [])

  const checkUser = () => {
    if(sessionStorage.getItem('access_token')){
      setCurrentUser(sessionStorage.getItem('access_token'))
    }
  } 

  return (
    <div>

      {
        !!currentUser ? (
          <div>
            <button onClick={logout}>
              Logout
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <input type="text" id="username" onChange={(e) => setUsername(e.target.value)} value={username} placeholder='username' />
            <input type="password" id="password" onChange={(e) => setPassword(e.target.value)} value={password} placeholder='password' />
            <button>Login</button>
          </form>
        )
      }
    </div>
  )
}

export default App