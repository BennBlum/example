using System.Collections.Generic;
using System.Linq;
using Lib.AutoReply.Actions;
using Lib.AutoReply.Classes;

namespace Lib.AutoReply.ResponseHandlers.Rental
{
    public class AgentResponseHandler : BaseResponseHandler
    {
        public AgentResponseHandler(TextEncoder encoder) : base(encoder)
        {

        }

        protected override void IdentifyPatterns(AutoReplyContext context)
        {
            context.Patterns = new Dictionary<AutoReplyPattern, bool>
            {
                { AutoReplyPattern.LeaseLength, context.ResponseList.Any(x => x.Intent == IntentType.LeaseLength) },
                { AutoReplyPattern.MoveInDate, context.ResponseList.Any(x => x.Intent == IntentType.MoveInDate) },
                { AutoReplyPattern.PropFeatures, context.ResponseList.Any(x => x.Intent == IntentType.PropFeatures) },
                { AutoReplyPattern.Rent, context.ResponseList.Any(x => x.Intent == IntentType.Rent) }
            };
        }

        protected override void MapPatternToResponse(AutoReplyContext context)
        {
            context.PatternMethods = new Dictionary<AutoReplyPattern, PatternResponseHandler>
            {
                { AutoReplyPattern.LeaseLength, HandleLeaseResponse },
                { AutoReplyPattern.MoveInDate, HandleMoveInDateResponse },
                { AutoReplyPattern.pFeatures, HandleFeaturesResponse },
                { AutoReplyPattern.Rent, HandleRentResponse }
            };
        }

        protected override void FinalizeResponse(AutoReplyContext context)
        {
            context.Handled = true;
        }

        private void HandleLeaseResponse(AutoReplyPattern pattern, AutoReplyContext context)
        {
            // Reponse logic goes here
        }

        private void HandleMoveInDateResponse(AutoReplyPattern pattern, AutoReplyContext context)
        {
            // Reponse logic goes here
        }

        private void HandleFeaturesResponse(AutoReplyPattern pattern, AutoReplyContext context)
        {
            // Reponse logic goes here
        }

        private void HandleRentResponse(AutoReplyPattern pattern, AutoReplyContext context)
        {
            // Reponse logic goes here
        }
    }
}
