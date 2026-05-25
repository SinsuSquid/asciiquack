const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

function activate(context) {
    const provider = new AsciiquackViewProvider(context.extensionUri);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(AsciiquackViewProvider.viewType, provider)
    );
}

class AsciiquackViewProvider {
    static viewType = 'asciiquack.view';

    constructor(extensionUri) {
        this._extensionUri = extensionUri;
    }

    resolveWebviewView(webviewView, context, _token) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);
    }

    _getHtmlForWebview(webview) {
        const htmlPath = path.join(this._extensionUri.fsPath, 'media', 'webview.html');
        try {
            return fs.readFileSync(htmlPath, 'utf8');
        } catch (err) {
            return `<html><body><h3>Error loading Asciiquack webview: ${err.message}</h3></body></html>`;
        }
    }
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
