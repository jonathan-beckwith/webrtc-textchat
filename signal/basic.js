//SignalServer based on localStorage
function SignalServer_Basic(room) {
    this.room = room || (Math.random()*100000000000000000).toString(36);
}
SignalServer_Basic.prototype.get = function (key, callback, error) {
    var error = error || function (r) { console.error(r); };

    try {
        callback(JSON.parse(
            localStorage.getItem(this.room + ':' + key)
        ));
    } catch (e) {
        error(e);
    }
};
SignalServer_Basic.prototype.set = function (key, value, callback, error) {
    var callback = callback || function (r) { console.log(r); },
        error = error || function (r) { console.error(r); };

    try {
        localStorage.setItem(
            this.room + ':' + key,
            JSON.stringify(value)
        );
        callback({ status: 'ok' });
    } catch (e) {
        error(e);
    }
};
SignalServer_Basic.prototype.poll = function (key, callback, error) {
    //Preserve context
    var self = this;

    this.get(key, function (data) {
        if(data === null) {
            console.warn('Could not get ' + self.room + ':' + key + ' retrying.');
            setTimeout(function () {
                self.poll(key, callback, error);
            }, 1000);
        } else {
            callback(data);
        }
    }, error);
};