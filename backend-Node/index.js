const express = require('express')
const cors = require('cors')
const port = 3000

const db = require('./database')
const bodyParser = require('body-parser')

app = express()

app.use(express.json())
app.use(bodyParser.urlencoded({ extended: true }))
app.use(cors())

// 检查连接
app.get('/', (req, res) => {
  res.send('hello world')
}) 

// 获取所有user
app.get('/admin/user', async(req, res) => {
  const result = await db.query('SELECT * FROM users')
  res.status(200).json({
    code: 200,
    data: result.rows,
    message: 'user form query success'
  })
})

// 用户注册
app.post('/user/register', async(req, res) => {
  const { name, email, password } = req.body
  const result = await db.query(
    "INSERT INTO users (name, email, password_hash) VALUES ($1, $2, $3) RETURNING name, email",
    [name, email, password]
  )
  res.status(200).json({
    code: 200,
    data: result.rows[0],
    message: 'insert success'
  })
})

app.post('/user/login', async(req, res) => {
  const { email, password } = req.body

  const result = await db.query(`SELECT id, name, email, password_hash FROM users WHERE email = $1`, [email])

  if (result.rows.length === 0) {
    return res.status(400).json({error: 'user email invalid'})
  }

  const user = result.rows[0]
  if (user.password_hash !== password) {
    return res.status(400).json({ error: '密码错误' })
  }

  res.status(200).json({
    message: '登录成功',
    user: { id: user.id, name: user.name, email: user.email, role: user.role }
  })

})

// 监听端口
app.listen(port, () => {
  console.log(`listening on port: ${port}`)
})