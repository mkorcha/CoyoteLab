/**
 * A fairly heavily modified verson of WSSHClient that is part of the wssh 
 * Python package. The original can be found in 
 * site_packages/wssh/static/wssh.js in the virtualenv donwload files
 */

function WSSHClient() {};

WSSHClient.prototype.connect = function(endpoint, options) {
    if (window.WebSocket) {
        this._connection = new WebSocket(endpoint);
    }
    else if (window.MozWebSocket) {
        this._connection = MozWebSocket(endpoint);
    }
    else {
        options.onError('WebSocket Not Supported');
        return ;
    }

    this._connection.onopen = function() {
        options.onConnect();
    };

    this._connection.onmessage = function (evt) {
        var data = JSON.parse(evt.data.toString());
        if (data.error !== undefined) {
            options.onError(data.error);
        }
        else {
            options.onData(data.data);
        }
    };

    this._connection.onclose = function(evt) {
        options.onClose();
    };
};

WSSHClient.prototype.send = function(data) {
    this._connection.send(JSON.stringify({'data': data}));
};
