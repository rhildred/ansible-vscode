import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse

app = FastAPI()

# Reuse a single async client for connection pooling
async_client = httpx.AsyncClient(base_url="http://localhost")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def dynamic_proxy(request: Request, path: str):
    # 1. Extract host header (e.g., "4040.test.example.com")
    host_header = request.headers.get("host", "")
    
    try:
        # 2. Parse the port number from the first subdomain segment
        port_str = host_header.split(".")[0]
        port = int(port_str)
    except (ValueError, IndexError):
        return Response(content="Invalid port in subdomain structure", status_code=400)

    # 3. Construct target local URL
    # request.url.path includes the leading slash, query includes parameters
    query_params = f"?{request.url.query}" if request.url.query else ""
    target_url = f"http://localhost:{port}{request.url.path}{query_params}"

    # 4. Prepare stream payload from incoming request
    headers = dict(request.headers)
    headers.pop("host", None)  # Let httpx handle the new host header
    
    # 5. Forward request asynchronously and stream the response back
    req = async_client.build_request(
        method=request.method,
        url=target_url,
        headers=headers,
        content=request.stream(),
    )
    
    rp_resp = await async_client.send(req, stream=True)
    
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=dict(rp_resp.headers),
        background=rp_resp.aclose,
    )
