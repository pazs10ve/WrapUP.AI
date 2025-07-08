# WrapUp.AI Product Requirements Document

## Executive Summary

WrapUp.AI is an AI-powered meeting assistant that automatically joins Google Meet sessions, transcribes conversations in real-time, and generates comprehensive meeting summaries with action items. The product eliminates manual note-taking and ensures all participants receive professional meeting documentation via email.

## Product Overview

### Vision Statement
Transform how teams capture and share meeting insights by automating the entire process from transcription to distribution.

### Problem Statement
- Teams waste time taking manual meeting notes
- Important action items and decisions get lost or forgotten
- Participants lack consistent meeting documentation
- Follow-up tasks are not properly tracked or assigned

### Solution
An AI bot that joins Google Meet sessions as a participant, processes conversations in real-time, and automatically distributes professional meeting summaries to all attendees.

## Target Audience

### Primary Users
- **Small to Medium Teams** (5-50 employees)
- **Remote/Hybrid Organizations** with frequent video meetings
- **Project managers** who need consistent meeting documentation
- **Startups** and **agencies** with limited administrative resources

### User Personas

#### Sarah - Project Manager
- Manages 10-15 meetings per week
- Needs to track action items across multiple projects
- Spends 2-3 hours weekly on meeting notes
- Values organization and follow-through

#### Mike - Startup Founder
- Attends investor meetings and team standups
- Needs professional documentation for stakeholders
- Limited time for administrative tasks
- Requires scalable solutions

## Product Goals

### Primary Goals
1. **Automate meeting documentation** with 95% accuracy
2. **Reduce administrative overhead** by 80% for meeting organizers
3. **Improve action item tracking** and follow-through
4. **Provide consistent professional documentation** across all meetings

### Success Metrics
- **User Adoption**: 100 active users in first 3 months
- **Meeting Processing**: 500+ meetings processed monthly
- **User Satisfaction**: 4.5+ star rating
- **Retention Rate**: 70% monthly active users
- **Processing Accuracy**: 95% transcription accuracy

## Core Features

### MVP Features (Phase 1)

#### 1. Bot Meeting Participant
- **Functionality**: Automated bot joins Google Meet sessions
- **User Experience**: 
  - Remains muted throughout meeting
  - Takes notes of the meeting
  - Exits gracefully when meeting ends
- **Technical Requirements**:
  - Puppeteer-based Google Meet integration
  - Reliable joining mechanism for various meeting formats
  - Resource management for concurrent meetings

#### 2. Real-time Transcription
- **Functionality**: Live speech-to-text conversion during meetings
- **User Experience**:
  - Invisible to meeting participants
  - Real-time processing with minimal delay
  - Speaker identification when possible
- **Technical Requirements**:
  - AssemblyAI integration for transcription
  - Audio capture from Google Meet
  - Streaming processing pipeline

#### 3. AI-Powered Analysis
- **Functionality**: Intelligent extraction of meeting insights
- **Output Format**:
  - Executive summary (2-3 sentences)
  - Key discussion points
  - Action items with assignees and deadlines
  - Next steps and follow-up items
- **Technical Requirements**:
  - Gemini integration for content analysis
  - Structured output formatting
  - Context-aware processing

#### 4. Automated Email Distribution
- **Functionality**: Professional meeting summaries sent to all participants
- **User Experience**:
  - Emails sent within 5 minutes of meeting end
  - Professional formatting with company branding
  - PDF attachment with detailed summary
- **Technical Requirements**:
  - Gmail API integration
  - Email template system
  - Participant email extraction

#### 5. Web Dashboard
- **Functionality**: Central hub for managing meetings and summaries
- **Features**:
  - Meeting history and summaries
  - Edit and customize summaries
  - User settings and preferences
  - Bot scheduling and management
- **Technical Requirements**:
  - React/Next.js frontend
  - Real-time updates via WebSocket
  - Responsive design

### Future Features (Phase 2+)

#### 1. Calendar Integration
- Auto-schedule bot for recurring meetings
- Google Calendar sync for meeting detection
- Meeting preparation insights

#### 2. Advanced Analytics
- Meeting insights and trends
- Team productivity metrics
- Action item completion tracking

#### 3. Integration Ecosystem
- Slack notifications and summaries
- Notion/Asana task creation
- CRM integration for client meetings

#### 4. Multi-platform Support
- Microsoft Teams integration
- Zoom support
- Generic video platform compatibility

## Technical Architecture

### System Architecture
```
Frontend (React/Next.js)
    ↓
API Gateway (Express/Node.js)
    ↓
Bot Manager (Puppeteer)
    ↓
Audio Processing (AssemblyAI)
    ↓
AI Analysis (Claude/GPT)
    ↓
Email Service (Gmail API)
    ↓
Database (PostgreSQL)
```

### Technology Stack

#### Frontend
- **Framework**: React/Next.js
- **Styling**: Tailwind CSS
- **State Management**: React Query + Context API
- **Real-time Updates**: WebSocket integration

#### Backend
- **Runtime**: Node.js
- **Framework**: Express.js
- **Database**: PostgreSQL
- **Cache**: Redis
- **Queue**: Bull Queue for job processing

#### AI Services
- **Speech-to-Text**: AssemblyAI
- **Content Analysis**: Claude 3.5 Sonnet
- **Email Processing**: Gmail API

#### Infrastructure
- **Hosting**: Digital Ocean/AWS
- **Containers**: Docker
- **Orchestration**: Docker Compose
- **Monitoring**: Basic logging and error tracking

### Data Models

#### Meeting
```sql
CREATE TABLE meetings (
    id UUID PRIMARY KEY,
    title VARCHAR(255),
    meeting_url VARCHAR(500),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    participants JSONB,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Transcript
```sql
CREATE TABLE transcripts (
    id UUID PRIMARY KEY,
    meeting_id UUID REFERENCES meetings(id),
    speaker VARCHAR(255),
    text TEXT,
    timestamp TIMESTAMP,
    confidence FLOAT
);
```

#### Summary
```sql
CREATE TABLE summaries (
    id UUID PRIMARY KEY,
    meeting_id UUID REFERENCES meetings(id),
    executive_summary TEXT,
    key_points JSONB,
    action_items JSONB,
    next_steps JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## User Experience

### User Journey

#### 1. Onboarding
1. User signs up with Google account
2. Grants necessary permissions (Gmail, Calendar)
3. Completes setup wizard
4. Schedules first meeting with bot

#### 2. Meeting Setup
1. User creates Google Meet
2. Invites WrapUp.AI bot to meeting
3. Bot confirms attendance
4. Meeting proceeds normally

#### 3. During Meeting
1. Bot joins meeting as participant
2. Real-time transcription begins
3. AI analysis runs in background
4. Bot remains unobtrusive

#### 4. Post-Meeting
1. Bot generates summary within 2 minutes
2. Email sent to all participants
3. Summary available in dashboard
4. User can edit and customize

### User Interface Design

#### Dashboard Layout
- **Header**: Navigation, user profile, settings
- **Main Content**: Meeting list, recent summaries
- **Sidebar**: Quick actions, statistics
- **Footer**: Support links, documentation

#### Meeting Summary View
- **Header**: Meeting details, participants
- **Content**: Executive summary, key points, action items
- **Actions**: Edit, export, share, schedule follow-up

## Business Model

### Pricing Strategy

#### Free Tier
- **Limit**: 5 meetings per month
- **Features**: Basic transcription and summaries
- **Target**: Individual users and small teams

#### Pro Tier ($15/month)
- **Limit**: 50 meetings per month
- **Features**: Advanced AI analysis, custom templates
- **Target**: Growing teams and professionals

#### Enterprise Tier ($50/month)
- **Limit**: Unlimited meetings
- **Features**: Custom integrations, priority support
- **Target**: Large organizations

### Revenue Projections
- **Month 1-3**: Focus on user acquisition (Free tier)
- **Month 4-6**: Convert 20% to Pro tier
- **Month 7-12**: Target $5K MRR with 100+ Pro users

## Risk Assessment

### Technical Risks
1. **Google Meet API Changes**: Mitigation through robust error handling
2. **AI Service Reliability**: Backup providers and fallback mechanisms
3. **Audio Quality Issues**: Preprocessing and enhancement algorithms
4. **Scaling Challenges**: Horizontal scaling architecture

### Business Risks
1. **Competition**: Focus on superior user experience
2. **Privacy Concerns**: Clear data policies and security measures
3. **Compliance**: GDPR/CCPA compliance from day one
4. **Market Adoption**: Extensive user testing and feedback loops

## Success Criteria

### Technical Success
- **Uptime**: 99.5% system availability
- **Accuracy**: 95% transcription accuracy
- **Performance**: <30 second processing time
- **Scalability**: Support 100+ concurrent meetings

### Business Success
- **User Growth**: 1000+ registered users in 6 months
- **Revenue**: $10K MRR by end of year 1
- **User Satisfaction**: 4.5+ star rating
- **Retention**: 70% monthly active users

## Timeline

### Phase 1 (Months 1-3) - MVP Development
- **Month 1**: Core bot infrastructure and Google Meet integration
- **Month 2**: AI processing pipeline and basic dashboard
- **Month 3**: Email integration and user testing

### Phase 2 (Months 4-6) - Enhancement & Growth
- **Month 4**: Advanced features and UI improvements
- **Month 5**: Marketing launch and user acquisition
- **Month 6**: Performance optimization and scaling

### Phase 3 (Months 7-12) - Scale & Expand
- **Months 7-9**: Additional integrations and enterprise features
- **Months 10-12**: Geographic expansion and partnership development

## Conclusion

WrapUp.AI addresses a clear market need for automated meeting documentation. With a solid technical foundation using AssemblyAI for transcription and a bot-participant approach for Google Meet integration, the product is positioned for rapid development and market validation.

The MVP focuses on core functionality that delivers immediate value to users while building a foundation for future growth and feature expansion. Success depends on execution quality, user experience, and strategic market positioning.

---

*Document Version: 1.0*  
*Last Updated: July 2025*  
*Next Review: August 2025*