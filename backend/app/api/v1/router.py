from fastapi import APIRouter
from app.api.v1.endpoints import me, classify, chat, history, document, alerts, stripe, conversations, auth, document_search, intelligent_templates, proactive_suggestions, attachments, calculator

api_router = APIRouter()

# Include endpoint modules
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(me.router, prefix="/me", tags=["me"])
api_router.include_router(classify.router, prefix="/classify", tags=["classify"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(history.router, prefix="/history", tags=["history"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(document.router, prefix="/document", tags=["document"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(stripe.router, prefix="/stripe", tags=["stripe"])
api_router.include_router(document_search.router, prefix="/documents", tags=["document-search"])
api_router.include_router(intelligent_templates.router, prefix="/templates", tags=["intelligent-templates"])
api_router.include_router(proactive_suggestions.router, prefix="/suggestions", tags=["proactive-suggestions"])
api_router.include_router(attachments.router, prefix="/attachments", tags=["attachments"])
api_router.include_router(calculator.router, prefix="/calculator", tags=["calculator"])
