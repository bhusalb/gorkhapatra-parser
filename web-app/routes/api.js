var express = require('express');
var fs = require('fs');
var path = require('path');
var crypto = require('crypto'),
    algorithm = 'aes-256-ctr',
    password = 'assaas';

function encrypt(text) {
    var cipher = crypto.createCipher(algorithm, password);
    var crypted = cipher.update(text, 'utf8', 'hex');
    crypted += cipher.final('hex');
    return crypted;
}

function decrypt(text) {
    var decipher = crypto.createDecipher(algorithm, password);
    var dec = decipher.update(text, 'hex', 'utf8');
    dec += decipher.final('utf8');
    return dec;
}

function apiMiddleware(req, res, next) {
    if (req.headers.slogan === 'easy-access-to-information') {
        req.isAPI = true;
        return next();
    }
    return res.status(404).send({status: false, msg: 'invalid request'});
};


var router = express.Router();

/* GET users listing. */
router.post('/notices', apiMiddleware, function (req, res, next) {
    var date = req.body.date || new Date().toJSON().slice(0, 10);
    var image_folder_path = path.join(__dirname, '../../images/' + date);
    fs.readdir(image_folder_path, function (err, items) {
        if (!items)
            return res.status(404).end();

        var encoded_items = [];
        items.forEach(function (item) {
            encoded_items.push(encrypt(image_folder_path + '/' + item));
        });

        res.json(encoded_items);
    });

    // res.send(date);
    //
    // res.send('respond with a resource');
});

router.get('/notices/:id/thumb', function (req, res, next) {
    return get_notice_image(req, res, true);
});

router.get('/notices/:id', function (req, res, next) {
    return get_notice_image(req, res);
});


function get_notice_image(req, res, thumb = false) {
    try {
        var image_path = decrypt(req.params.id);
    } catch (e) {
        return res.status(404).end();
    }

    if (thumb) {
        var dirs = image_path.split('/');
        dirs[dirs.length - 1] = 'thumbs/' + dirs[dirs.length - 1];
        image_path = dirs.join('/');
    }


    fs.stat(image_path, function (err, exists) {
        if (!err)
            return res.sendfile(image_path);

        res.status(404);
    });
}

module.exports = router;
