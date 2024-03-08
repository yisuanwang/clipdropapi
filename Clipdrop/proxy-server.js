const express = require('express');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
// require('dotenv').config(); // 用于从 .env 文件中读取环境变量


const app = express();
const PORT = 3000;
const CLIPDROP_API_URL = 'https://clipdrop-api.co/cleanup/v1';
const API_KEY = '5ec050c2f0a57ef6d5cfad7e302479fa745275e79f0d9b0ecd73ccae383787e2054ed81a78f59ac3e416c066952f3f02';
// 3fde43c5cecba030f11187fe643e619576f7eea915500515b8aba9305531bf4ab8746698fdf948e51e6c4960722ec1bd

app.use(express.json());

app.post('/cleanup', async (req, res) => {
    console.log(`dddddddddddddddddddd ${req}`);
    try {
        const { image, mask } = req.body;

        const formData = new FormData();
        formData.append('image_file', fs.createReadStream(image));
        formData.append('mask_file', fs.createReadStream(mask));

        const response = await axios.post(CLIPDROP_API_URL, formData, {
            headers: {
                ...formData.getHeaders(),
                'x-api-key': API_KEY
            },
            maxContentLength: Infinity,
            maxBodyLength: Infinity
        });

        res.set(response.headers);
        res.status(response.status).send(response.data);
    } catch (error) {
        if (error.response) {
            res.status(error.response.status).send(error.response.data);
        } else {
            res.status(500).send({ error: 'Internal server error' });
        }
    }
});

app.listen(PORT, () => {
    console.log(`Proxy server is running on port ${PORT}`);
});
