
const CryptoJS = require("crypto-js");


function aesDecryptBase64( strKey, strEncText, strIv ){

    strEncText = ( strEncText + "").replace(/\n*$/g, "").replace(/\n/g, "");


    const key = CryptoJS.enc.Base64.parse( strKey );
    var iv = key;
    if( strIv && strIv.length > 0 ) {
        var iv = CryptoJS.enc.Base64.parse( strIv );
    }

    const t = CryptoJS.enc.Base64.parse( strEncText )
          , n = CryptoJS.enc.Base64.stringify(t);

    const decryptedBytes = CryptoJS.AES.decrypt( n, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });


    return decryptedBytes.toString(CryptoJS.enc.Utf8).toString()
}


function aesDecrypt( strKey, strEncText, strIv ){

    strEncText = ( strEncText + "").replace(/\n*$/g, "").replace(/\n/g, "");

    const key = CryptoJS.enc.Utf8.parse( strKey );
    const iv = key
    if( strIv && strIv.length > 0 ) {
        const iv = CryptoJS.enc.Utf8.parse( strIv );
    }

    const decryptedBytes = CryptoJS.AES.decrypt( strEncText, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });


    return decryptedBytes.toString(CryptoJS.enc.Utf8);
}

