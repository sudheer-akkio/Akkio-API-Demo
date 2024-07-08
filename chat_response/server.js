const express = require('express');
const app = express();
const path = require('path');

// Serve static files (HTML, CSS, JS) from the 'public' folder
app.use(express.static(path.join(__dirname)));

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});