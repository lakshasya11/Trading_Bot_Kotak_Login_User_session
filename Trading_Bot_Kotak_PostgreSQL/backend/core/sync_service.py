class ClientBotSync:
    """Handles syncing session data to central server"""
    
    def sync_session_to_central(self, session_payload: dict):
        """Sync session data to central server (PC2)"""
        try:
            # TODO: Implement actual sync logic when central server is ready
            print(f"[Sync] Would sync session: {session_payload.get('client_id')} - {session_payload.get('mode')}")
        except Exception as e:
            print(f"[Sync] Error syncing to central: {e}")
