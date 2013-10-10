
//SignalServer based on OpenKeyVal v 1.1
//  http://openkeyval.org/

function SignalServer_OpenKeyVal(room) {
    this.room = room || (Math.random()*100000000000000000).toString(36);
}
SignalServer_OpenKeyVal.prototype.get = function (key, callback, error) {
    remoteStorage.getItem(this.room + ':' + key, callback);
};
SignalServer_OpenKeyVal.prototype.set = function (key, value, callback, error) {
    var callback = callback || function (r) { console.log(r); },
        error = error || function (r) { console.error(r); };

    try {
        remoteStorage.setItem(
            this.room + ':' + key,
            JSON.stringify(value)
        );
        callback({ status: 'ok' });
    } catch (e) {
        error(e);
    }
};
SignalServer_OpenKeyVal.prototype.poll = function (key, callback, error) {
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