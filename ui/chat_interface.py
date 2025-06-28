# ui/chat_interface.py
import streamlit as st
import requests
import json
from config import API_BASE_URL
from utils.helpers import reset_chat, logout, handle_suggestion_click

def render_chat_interface():
    render_sidebar()
    st.markdown(
        """
        <style>
        /* Align chat left, next to the sidebar */
        .main .block-container {
            max-width: 800px;
            margin-left: 0px
            padding-left: 1rem;
            padding-right: 1rem;
        }
        @media (max-width: 1200px) {
            .main .block-container {
                margin-left: 0 !important;
                max-width: 100vw !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
   
    st.title("Helion Scheduling Concierge")
    st.caption("Advanced collaboration scheduling for fusion energy innovation")
   
    if not st.session_state.history:
        render_welcome_section()
    
    for msg in st.session_state.history:
        role = "user" if msg.get("type") == "human" else "assistant"
        with st.chat_message(role):
            if role == "assistant" and "run_details" in msg and msg["run_details"]:
                with st.status("Agent Process", expanded=False, state="complete"):
                    for step in msg["run_details"]:
                        st.markdown(f"✅ {step['name']}", unsafe_allow_html=True)
            
            st.markdown(msg.get("content", ""))

    handle_chat_input()

    if st.session_state.history and st.session_state.history[-1]["type"] == "human":
        if not st.session_state.get("agent_is_replying", False):
            st.session_state.agent_is_replying = True
            prompt = st.session_state.history[-1]["content"]
            stream_agent_response(prompt)
            st.session_state.agent_is_replying = False
            st.rerun()

def render_sidebar():
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            max-width: 350px !important;
            width: 350px !important;
            min-width: unset !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; padding: 1.5rem 0; border-bottom: 1px solid #333; margin-bottom: 2rem;">
                <h2 style="margin: 0; color: #00d4ff; font-weight: 300; font-size: 2rem;">HELION</h2>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #888; letter-spacing: 1px;">
                    FUSION ENERGY
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%); 
                        padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid #333;">
                <h4 style="margin: 0 0 1rem 0; color: #00d4ff; font-weight: 500;">User Profile</h4>
                <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #888; font-size: 0.85rem;">Name</span>
                        <span style="color: white; font-weight: 500;">{}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #888; font-size: 0.85rem;">Email</span>
                        <span style="color: white; font-weight: 400; font-size: 0.85rem;">{}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #888; font-size: 0.85rem;">Timezone</span>
                        <span style="color: #00d4ff; font-weight: 500;">{}</span>
                    </div>
                </div>
            </div>
            """.format(
                st.session_state.get('username', 'N/A').title(),
                st.session_state.get('email', 'N/A'),
                st.session_state.get('timezone', 'UTC').upper()
            ),
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #0a1a1f 0%, #1a2f3a 100%); 
                        padding: 1.5rem; border-radius: 12px; border: 1px solid #2a4a5a;">
                <h4 style="margin: 0 0 1rem 0; color: #00d4ff; font-weight: 500;">Scheduling Concierge</h4>
                <p style="color: #b8c2cc; line-height: 1.5; margin-bottom: 1.2rem; font-size: 0.9rem;">
                    Facilitating collaboration across our fusion research initiatives. 
                    Schedule meetings with engineers, scientists, partners, and stakeholders.
                </p>
                <div style="background: rgba(0, 212, 255, 0.1); padding: 1rem; border-radius: 8px; border-left: 3px solid #00d4ff;">
                    <h5 style="margin: 0 0 0.8rem 0; color: #00d4ff; font-size: 0.9rem;">Core Capabilities</h5>
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="color: #00d4ff; font-size: 0.8rem;">●</span><span style="color: #b8c2cc; font-size: 0.85rem;">Meeting coordination & scheduling</span></div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="color: #00d4ff; font-size: 0.8rem;">●</span><span style="color: #b8c2cc; font-size: 0.85rem;">Calendar management & availability</span></div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="color: #00d4ff; font-size: 0.8rem;">●</span><span style="color: #b8c2cc; font-size: 0.85rem;">Cross-timezone optimization</span></div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;"><span style="color: #00d4ff; font-size: 0.8rem;">●</span><span style="color: #b8c2cc; font-size: 0.85rem;">Resource allocation assistance</span></div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="small")
        with col1:
            st.button("Clear History", on_click=reset_chat, use_container_width=True)
        with col2:
            st.button("Sign Out", on_click=logout, use_container_width=True, type="primary")

def render_welcome_section():
    st.markdown(
        """
        <div style="padding: 2.5rem; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); 
                    border-radius: 16px; margin: 1.5rem 0; color: white; border: 1px solid rgba(255,255,255,0.1);">
            <h3 style="margin: 0 0 1.5rem 0; color: #00d4ff; font-weight: 600; font-size: 1.5rem;">Welcome to Helion Energy</h3>
            <p style="margin: 0 0 2rem 0; line-height: 1.6; opacity: 0.9; font-size: 0.95rem;">
                I'm your AI-powered scheduling concierge. Select a suggestion below or type your own request.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown("#### Try asking me one of these:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🗓️ View my schedule for tomorrow", on_click=handle_suggestion_click, args=["Show me my upcoming meetings for tomorrow"], use_container_width=True)
        st.button("🤝 Find team availability", on_click=handle_suggestion_click, args=["Is there a 30 minute slot available with the engineering team next week?"], use_container_width=True)
    with col2:
        st.button("📅 Schedule a technical review", on_click=handle_suggestion_click, args=["Schedule a 45 minute technical review for tomorrow afternoon"], use_container_width=True)
        st.button("🔄 Reschedule a meeting", on_click=handle_suggestion_click, args=["Can you reschedule my event?"], use_container_width=True)

def handle_chat_input():
    if prompt := st.chat_input("Schedule a meeting..."):
        st.session_state.history.append({"type": "human", "content": prompt})
        st.rerun()

def stream_agent_response(prompt):
    with st.chat_message("assistant"):
        text_placeholder = st.empty()
        agent_steps = []
        full_response = ""
        generating_answer_step_added = False
            
        try:
            with st.status("Agent is working...", expanded=True) as status:
                steps_placeholder = st.empty()
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                payload = {"input": prompt, "history": st.session_state.history[:-1]}
           
                with requests.post(f"{API_BASE_URL}/chat/stream", json=payload, headers=headers, stream=True) as response:
                    response.raise_for_status()
                    for line in response.iter_lines():
                        if not line or line.strip() == b'data: [DONE]': continue
                        data_str = line.decode('utf-8').removeprefix('data: ')
                        try: data = json.loads(data_str)
                        except json.JSONDecodeError: continue
                       
                        event_type = data.get('type')
                        
                        if event_type == 'tool_start':
                            if agent_steps and agent_steps[-1]['status'] == 'running':
                                agent_steps[-1]['status'] = 'complete'
                            
                            tool_name = data.get('name', 'Unknown tool')
                            tool_name_html = f"<span style='color: #2df299; font-family: monospace; background-color: rgba(45, 242, 153, 0.1); padding: 2px 6px; border-radius: 4px; font-weight: 400;'>{tool_name}</span>"
                            agent_steps.append({'name': f"Calling tool: {tool_name_html}", 'status': 'running'})
                            
                            steps_html = "".join([f"<div>{'✅' if s['status'] == 'complete' else '⚙️'} {s['name']}</div>" for s in agent_steps])
                            steps_placeholder.markdown(steps_html, unsafe_allow_html=True)

                        elif event_type == 'token':
                            if not generating_answer_step_added:
                                if agent_steps and agent_steps[-1]['status'] == 'running':
                                    agent_steps[-1]['status'] = 'complete'
                                agent_steps.append({'name': "Generating final answer", 'status': 'running'})
                                generating_answer_step_added = True
                                
                                steps_html = "".join([f"<div>{'✅' if s['status'] == 'complete' else '⚙️'} {s['name']}</div>" for s in agent_steps])
                                steps_placeholder.markdown(steps_html, unsafe_allow_html=True)
                            
                            full_response += data.get('content', '')
                            text_placeholder.markdown(full_response + "▌")
            
            if agent_steps:
                agent_steps[-1]['status'] = 'complete'
            status.update(label="Process Complete!", state="complete", expanded=False)
            
            with status:
                steps_html = "".join([f"<div>✅ {s['name']}</div>" for s in agent_steps])
                st.markdown(steps_html, unsafe_allow_html=True)

            text_placeholder.markdown(full_response)
            
            ai_message_to_save = {
                "type": "ai",
                "content": full_response,
                "run_details": agent_steps,
            }
            st.session_state.history.append(ai_message_to_save)
            
        except requests.RequestException as e:
            error_message = f"Connection interrupted. Please verify your network connection and try again. Technical details: {e}"
            text_placeholder.error(error_message)
            st.session_state.history.append({"type": "ai", "content": error_message, "run_details": []})