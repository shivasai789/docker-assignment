const express = require('express');
const path = require('path');
const axios = require('axios');
const bodyParser = require('body-parser');

const app = express();
const FLASK_BACKEND = process.env.BACKEND_URL || 'http://127.0.0.1:5000'; // Flask backend URL

// Configuration
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(bodyParser.urlencoded({ extended: true }));

// Routes
app.get('/', (req, res) => {
  res.render('form');
});

app.post('/submit', async (req, res) => {
  try {
    const { name, email, message } = req.body;
    
    // Send data to Flask backend
    const response = await axios.post(`${FLASK_BACKEND}/process-form`, {
      name,
      email, 
      message
    });

    // Render result with Flask's response
    res.render('result', { 
      originalData: req.body,
      processedData: response.data 
    });
    
  } catch (error) {
    console.error('Error contacting backend:', error);
    res.status(500).send('Error processing your form');
  }
});

app.listen(3000, () => {
  console.log('Frontend running on http://localhost:3000');
});