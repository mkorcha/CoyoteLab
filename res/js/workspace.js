Terminal.prototype.wssh = function(wsendpoint) {
	/**
	 * Adds connection to wssh capability to the Terminal object by setting up
	 * the custom handlers the WSSHClient requires
	 */
	var client = new WSSHClient(),
	    term = this;

	this.write('Connecting...');

	this.on('key', function(key) {
		client.send(key);
	});

	client.connect(wsendpoint, {
		onError: function(error) {
			term.write('Error: ' + error + '\r\n');
		},
		onConnect: function() {
			// Erase our connecting message
			term.write('\r');
		},
		onClose: function() {
			term.write('Connection Reset By Peer');
		},
		onData: function(data) {
			term.write(data);
		}
	});
}

function workspace_init(element, endpoint) {
	/**
	 * Creates a new Terminal object and embeds it into the given element,
	 * connected to the given websocket endpoint directed to wssh
	 */
	var term = new Terminal({cursorBlink: true});

	term.open(element);
	term.fit()

	term.wssh(endpoint);
}

function fix_prefix(endpoint) {
	/**
	 * Moves around some flask limitations and enforces that if we're using
	 * HTTPS, everything will conform
	 */
	endpoint = endpoint.replace('ws://', '').replace('wss://', '').replace('http://', '').replace('https://', '');

	if(window.location.href.indexOf('https://') == 0) {
		return 'wss://' + endpoint;
	}

	return 'ws://' + endpoint;
}
