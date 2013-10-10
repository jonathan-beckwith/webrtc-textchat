//Connect to the demo signal server.
function SignalServer_Python(room) {
    this.room = room || (Math.random()*100000000000000000).toString(36);
    this.server = 'http://localhost:8080/';
}
SignalServer_Python.prototype.request = function (method, data, callback, error) {
    var xhr = new XMLHttpRequest(),
        data = data ? JSON.stringify(data) : undefined,
        callback = callback || function (r) { console.log(r); },
        error = error || function (r) { console.error(r); };

    xhr.open('POST', this.server + method);
    xhr.setRequestHeader(
        'Content-Type',
        'application/json'
    );

    xhr.onreadystatechange = function () {
        //We only care about when the request is finished.
        if(xhr.readyState !== 4) { return; }
        if(xhr.status === 200) {
            callback(JSON.parse(xhr.responseText));
        } else {
            error('ERROR::' + xhr.status + ':' + xhr.statusText);
        }
    }

    xhr.send(data);
}
SignalServer_Python.prototype.set = function (key, value, callback, error) {
    this.request(
        'set',
        { 'id': this.room + ':' + key, 'data': value },
        callback,
        error
    );
}
SignalServer_Python.prototype.get = function (key, callback, error) {
    var self = this;
    this.request(
        'get',
        { 'id': this.room + ':' + key },
        callback,
        error
    );
}
SignalServer_Python.prototype.poll = function (key, callback, error) {
    //preserve this
    var self = this;

    this.get(
        key,
        callback,
        function (message) {
            setTimeout(function () {
                self.poll(key, callback, error)
            }, 500);
        }
    );
}