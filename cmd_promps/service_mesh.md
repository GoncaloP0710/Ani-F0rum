Command to initialize the linkerd setup

    curl -sL https://run.linkerd.io/install | sh

Add the linkerd CLI to your path with:

    export PATH=$PATH:/home/areis04_net/.linkerd2/bin

Now run:

    # install the GatewayAPI CRDs
    kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.1/standard-install.yaml

    linkerd check --pre                                                   # validate that Linkerd can be installed
    linkerd install --crds | kubectl apply -f -                           # install the Linkerd CRDs
    linkerd install --set proxyInit.runAsRoot=true | kubectl apply -f -   # install the control plane into the 'linkerd' namespace (need root permission for docker container runtime and proxy-init container, since they must run as root user)
    linkerd check                                                         # validate everything worked!

You can also obtain observability features by installing the viz extension:

    linkerd viz install | kubectl apply -f -                        # install the viz extension into the 'linkerd-viz' namespace
    linkerd viz check                                               # validate the extension works!
    kubectl annotate namespace default linkerd.io/inject=enabled    # the .yml approach is instable so we inject it manually
    linkerd viz dashboard                                           # launch the dashboard
    # Open the localhost in the port showing in the console

Just in case we start the miscrosservices earlier:
  
    kubectl rollout restart deploy -n default   # restart and initialize new pods